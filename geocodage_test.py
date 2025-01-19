import requests
import psycopg2
from psycopg2 import sql

# Configuration de l'API et de PostgreSQL
API_URL = "https://api-adresse.data.gouv.fr/search/"
# Connexion à la base de données
POSTGRES_CONFIG= {
        'dbname': 'sap',
        'user': 'ludo',
        'password': 'test',
        'host': 'localhost',
        'port': '5432',
        'options' : '-c search_path=test'
    }

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


def insert_into_postgis(address, lon, lat):
    try:
        if lon is None or lat is None:
            print(f"Coordonnées manquantes pour l'adresse : {address}")
            return

        connection = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = connection.cursor()
        # Insérer dans la table
        print(f"Debug: lon={lon}, lat={lat}, type(lon)={type(lon)}, type(lat)={type(lat)}")
        lon = float(lon)
        lat = float(lat)

        query = sql.SQL("""
            INSERT INTO test.geocoded_addresses (address, lon, lat, geom)
       VALUES (%s, %s, %s, public.ST_SetSRID(public.ST_Point(%s::double precision, %s::double precision), 4326))
""")
        cursor.execute(query, (address, float(lon), float(lat), float(lon), float(lat)))

        connection.commit()
        cursor.close()
        connection.close()
        print(f"Adresse '{address}' géocodée et insérée avec succès.")
    except Exception as e:
        print("Erreur lors de l'insertion dans PostGIS :", e)

if __name__ == "__main__":
    adresse = "5 rue Emile Blémont, 75018 Paris, France"
    lon, lat = geocode_address(adresse)
    id = 1
    if lon is not None and lat is not None:
        insert_into_postgis(adresse, lon, lat)
    else:
        print(f"Impossible de géocoder l'adresse : {adresse}")
