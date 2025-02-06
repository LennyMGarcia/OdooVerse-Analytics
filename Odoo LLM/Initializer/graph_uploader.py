import requests

GRAPHDB_URL = "http://desktop-2kol6qd:7200/repositories/Odoo-BasicLLM-Repository/statements"

TTL_FILE_PATH = "data.ttl"

headers = {
    "Content-Type": "application/x-turtle"  
}

with open(TTL_FILE_PATH, "rb") as ttl_file:
    data = ttl_file.read()
    
    response = requests.post(GRAPHDB_URL, headers=headers, data=data)

    if response.status_code == 204:
        print("Datos cargados correctamente a GraphDB.")
    else:
        print(f"Error al cargar los datos: {response.status_code} - {response.text}")

