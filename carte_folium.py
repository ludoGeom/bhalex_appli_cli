import requests
import folium
from flask import Flask, render_template_string, request
import geocodage_v2 as gcd

def carteFolium():
    # === INITIALISATION DE L'APP FLASK ===
    app = Flask(__name__)

    # === TEMPLATE HTML POUR L'INTERFACE WEB ===
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vérification de l'adresse</title>
        {{ map|safe }}
        <script>
            function updateCoordinates(e) {
                document.getElementById('lat').value = e.latlng.lat;
                document.getElementById('lon').value = e.latlng.lng;
            }
        </script>
    </head>
    <body>
        <h2>Déplacez le marqueur si nécessaire, puis validez :</h2>
        <form action="/save" method="post">
            <label>Adresse : <input type="text" name="address" value="{{ address }}" readonly></label><br>
            <label>Latitude : <input type="text" id="lat" name="lat" value="{{ lat }}"></label><br>
            <label>Longitude : <input type="text" id="lon" name="lon" value="{{ lon }}"></label><br>
            <button type="submit">Enregistrer</button>
        </form>
    </body>
    </html>
    """

    # === AFFICHER LA CARTE INTERACTIVE ===
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            address = request.form["address"]
            lon, lat = gcd.geocode_address(address)

            if lon is None or lat is None:
                return "⚠️ Adresse introuvable !"

            # Création de la carte Folium
            map_object = folium.Map(location=[lat, lon], zoom_start=17)
            marker = folium.Marker([lat, lon], draggable=True)
            marker.add_child(folium.Popup("Déplacez-moi si nécessaire !"))
            marker.add_child(folium.LatLngPopup())  # Permet de récupérer les nouvelles coordonnées
            map_object.add_child(marker)

            # Génération du HTML
            map_html = map_object._repr_html_()

            return render_template_string(HTML_TEMPLATE, map=map_html, address=address, lat=lat, lon=lon)

        return '''
            <form action="/" method="post">
                <label>Entrez une adresse : <input type="text" name="address" required></label>
                <button type="submit">Géocoder</button>
            </form>
        '''


    # # === ENREGISTRER LES COORDONNÉES MODIFIÉES ===
    # @app.route("/save", methods=["POST"])
    # def save():
    #     address = request.form["address"]
    #     lat = request.form["lat"]
    #     lon = request.form["lon"]
    #
    #     if insert_into_postgis(address, lon, lat):
    #         return f"✅ Adresse enregistrée : {address} ({lat}, {lon})"
    #     else:
    #         return "❌ Erreur lors de l'enregistrement."


    # === LANCEMENT DU SERVEUR FLASK ===
    if __name__ == "__main__":
        app.run(debug=True)