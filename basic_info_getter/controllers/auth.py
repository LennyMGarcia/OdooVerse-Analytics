import json
import requests

url = "http://localhost:8069"
db = "Base"
username = "Lennymgr27@gmail.com"
password = "423204"

# Autenticación
response = requests.post(f"{url}/web/session/authenticate", json={
    "jsonrpc": "2.0",
    "params": {
        "db": db,
        "login": username,
        "password": password
    }
})

session_data = response.json()
user_id = session_data.get("result", {}).get("uid", False)
if user_id:
    print(f"Autenticado como usuario ID {session_data}")
else:
    print("Error de autenticación")
