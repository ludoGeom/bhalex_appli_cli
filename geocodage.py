import requests
import psycopg2
from psycopg2 import sql

# Configuration de l'API et de PostgreSQL
API_URL = "https://api-adresse.data.gouv.fr/search/"

def geocode_address(address):
    try:
        params = {"q": address}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["features"]:
                coords = data["features"][0]["geometry"]["coordinates"]
                return coords[0], coords[1]  # Longitude, Latitude
        print(f"Aucune donnée trouvée pour l'adresse : {address}")
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
    return None, None


