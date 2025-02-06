import asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from SPARQLWrapper import SPARQLWrapper, JSON
import json

tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2-medium")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2-medium")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(host='localhost', port=6333)
sparql = SPARQLWrapper("http://desktop-2kol6qd:7200/repositories/Odoo-BasicLLM-Repository")

async def query_qdrant(user_query_vector):
    collections = ['sales_orders', 'order_lines', 'products', 'countries', 'crm']
    results = []
    
    for collection in collections:
        response = await asyncio.to_thread(qdrant_client.search, collection_name=collection, query_vector=user_query_vector, limit=10)
        if isinstance(response, list) and len(response) > 0:
            results.extend(response)
    
    return results

async def query_graphdb(qdrant_results):
    entity_uris = []
    for result in qdrant_results:
        payload = result.payload
        if 'order_id' in payload:
            entity_uris.append(f"ex:Sales_order_{payload['order_id']}")
        if 'lead_id' in payload:
            entity_uris.append(f"ex:CRM_{payload['lead_id']}")
        if 'id' in payload and "product" in payload.get('name', "").lower():
            entity_uris.append(f"ex:Product_{payload['id']}")
        if 'code' in payload:
            entity_uris.append(f"ex:Country_{payload['id']}")

    query = f"""
    PREFIX ex: <http://odoollm.org/>
    SELECT ?subject ?predicate ?object WHERE {{
        VALUES ?subject {{ {" ".join(entity_uris)} }}
        ?subject ?predicate ?object.
    }} 
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return await asyncio.to_thread(sparql.query().convert)

async def combine_results(qdrant_results, graphdb_results):
    combined = []
    for qdrant_result in qdrant_results:
        payload = qdrant_result.payload
        entity_id = payload.get('order_id') or payload.get('lead_id') or payload.get('id')
    
        related_data = [
            triple for triple in graphdb_results['results']['bindings']
            if f"ex:{triple['subject']['value'].split('_')[-1]}" == f"ex:{entity_id}"
        ]
        
        combined.append({
            'qdrant_data': payload,
            'graphdb_data': related_data
        })
    
    return combined

def generate_response(combined_results):
    context = ""
    for result in combined_results:
        context += f"> {result['qdrant_data']}\n"
        context += "> \n"
        for triple in result['graphdb_data'][:3]:
            context += f"- {triple['predicate']['value'].split('/')[-1]}: {triple['object']['value']}\n"
    
    prompt = f"""A continuación, utiliza esta información para proporcionar un resumen económico detallado que pueda ser entendido por un humano.

    Datos:
    {context}

    Respuesta:

     """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=200)
    outputs = model.generate(
        inputs['input_ids'], 
        attention_mask=inputs['attention_mask'],  
        max_new_tokens=500,  
        temperature=1.2,  
        do_sample=False,  
        pad_token_id=tokenizer.pad_token_id  
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

async def main(user_query):
    user_query_vector = embedding_model.encode(user_query).tolist()

    qdrant_results = await query_qdrant(user_query_vector)

    graphdb_results = await query_graphdb(qdrant_results)

    combined_results = await combine_results(qdrant_results, graphdb_results)

    response = generate_response(combined_results)
    return response

user_query = "¿Qué información tengo sobre Mylan Ramos, dimelo en espanol?"
response = asyncio.run(main(user_query))
print("Respuesta final:", response)
