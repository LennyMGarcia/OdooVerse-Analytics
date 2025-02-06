import uuid
import json
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, HnswConfigDiff
from sentence_transformers import SentenceTransformer
import aiohttp

async def safe_get(url, key, retries=3):
    async with aiohttp.ClientSession() as session:
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get(key, [])
                    else:
                        print(f"Error {response.status} al obtener datos de {url}, intento {attempt + 1}")
            except aiohttp.ClientError as e:
                print(f"Error de conexion al obtener datos de {url}, intento {attempt + 1}: {e}")
            await asyncio.sleep(2) 
    return []  

client = QdrantClient(host='localhost', port=6333, timeout=300)

vector_size = 384  
distance = "Cosine"
collections = {
    'sales_orders': ['order_id', "partner_invoice", "partner_shipping", "date_order", "state", "amount_untaxed", "amount_tax", "amount_total", "country_code"],
    'order_lines': ['id', "product_name", "quantity", "unit_price", "subtotal"],
    'products': ['id', "name", "image_route"],
    'countries': ['id', "code", "name"],
    'crm': ['lead_id', "name", "email_from", "phone", "stage", "contact_name", "image_html"]
}

hnsw_config = HnswConfigDiff(
    m=16,
    ef_construct=100,
    full_scan_threshold=10000,
    max_indexing_threads=0,
    on_disk=True
)

async def create_collections_if_not_exist():
    for collection in collections.keys():
        if not client.collection_exists(collection_name=collection):
            client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=distance),
                hnsw_config=hnsw_config  
            )

model = SentenceTransformer('all-MiniLM-L12-v2')
batch_size = 50  

async def upsert_batch(collection_name, data_list, payload_fields):
    points = []
    for data in data_list:
        try:
            json_data = json.dumps(data, ensure_ascii=False) 
            vector = model.encode(json_data, convert_to_tensor=False).tolist()

            if len(vector) != vector_size:
                print(f"Error: El vector generado tiene una longitud de {len(vector)}, se esperaba {vector_size}.")
                continue

            unique_id = str(uuid.uuid4()) 

            points.append({
                'id': unique_id,
                'vector': vector,
                'payload': {field: data.get(field, None) for field in payload_fields}
            })

            
            if len(points) >= batch_size:
                print(f"Insertando {len(points)} puntos en {collection_name}...")
                await asyncio.to_thread(client.upsert, collection_name=collection_name, points=points)
                points = []  

        except Exception as e:
            print(f"Error en upsert_batch: {e}")

    if points:
        try:
            print(f"Insertando {len(points)} puntos finales en {collection_name}...")
            await asyncio.to_thread(client.upsert, collection_name=collection_name, points=points)
        except Exception as e:
            print(f"Error en upsert final: {e}")

async def insert_data():
    await create_collections_if_not_exist()

    api_data = {
        'sales_orders': await safe_get("http://localhost:8069/api/sales", "sales_orders"),
        'order_lines': await safe_get("http://localhost:8069/api/sales", "order_lines"),
        'products': await safe_get("http://localhost:8069/api/products", "Products"),
        'countries': await safe_get("http://localhost:8069/api/country", "Countries"),
        'crm': await safe_get("http://localhost:8069/api/crm", "CRM")
    }

    tasks = [
        upsert_batch(collection, api_data[collection], payload_fields)
        for collection, payload_fields in collections.items()
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(insert_data())
