import requests

urls = [
    "http://localhost:8069/api/products",
    "http://localhost:8069/api/crm",
    "http://localhost:8069/api/sales",
    "http://localhost:8069/api/country"
]

responses = {}
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        responses[url] = response.json()
    else:
        print(f"Error al obtener los datos de {url}")
