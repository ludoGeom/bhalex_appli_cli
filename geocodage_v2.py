import requests
import psycopg2
from psycopg2 import sql
import webbrowser

# Configuration de l'API et de PostgreSQL
API_URL = "https://api-adresse.data.gouv.fr/search/"
# === FONCTION POUR VÉRIFIER SUR GOOGLE MAPS ===
def open_google_maps(lon, lat):
    url = f"https://www.google.com/maps?q={lat},{lon}"
    webbrowser.open(url)

def geocode_address(adresse):
    try:
        params = {"q": adresse}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["features"]:
                coords = data["features"][0]["geometry"]["coordinates"]
                print(coords[0], coords[1])
                return coords[0], coords[1]  # Longitude, Latitude
        print(f"Aucune donnée trouvée pour l'adresse : {adresse}")
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return None, None

#geocode_address("5 rue emile blemont, 75018 paris")