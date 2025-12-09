import requests

# URL API local
url = "http://127.0.0.1:8000/api/profile/update/"

# Simulacion Token de Front
headers = {
    "Authorization": "Bearer TOKEN_DE_MENTIRA_123" 
}

# Datos a guardar que no guarda IreBase
payload = {
    "first_name": "Jean",
    "last_name": "Valjean",
    "company_name": "Sonido Master Loja", 
    "location": "Av. Universitaria"
}

# Petición POST
try:
    response = requests.post(url, json=payload, headers=headers)
    
    print("--- RESPUESTA DEL SERVIDOR ---")
    print(f"Status Code: {response.status_code}")
    print("JSON Recibido:")
    print(response.json())
    
    if response.status_code == 200:
        print("\n✅ ¡ÉXITO! El backend validó el token y guardó los datos extra.")
    else:
        print("\n❌ Algo falló.")

except Exception as e:
    print(f"Error de conexión: {e}")