
import geocodage
import tkinter as tk
from tkinter import messagebox, ttk
from geocodage_v2 import open_google_maps

def verif_adresse(adresse, entry_longitude=None, entry_latitude=None, combo_geocodage_bon=None):
    """
    Vérifie l'adresse et retourne ses coordonnées géographiques

    Args:
        address (str): L'adresse complète à vérifier

    Returns:
        tuple: (longitude, latitude) ou None en cas d'erreur
    """

    # Appel à la fonction de geocodage
    lon, lat = geocodage.geocode_address(adresse)
    print("dans verif_ad",adresse)
    print("dans verif_ad", lon, lat)
    # Ouverture Google Maps
    open_google_maps(lon, lat)
    if lon is None or lat is None:
        print("⚠️ Adresse introuvable !")
    else:
        print(f"📍 Coordonnées obtenues : {lat}, {lon}")


    geocodage_bon = combo_geocodage_bon.get()

    root = tk.Tk()
    root.title("Situation de l'adresse")
    root.geometry("400x500")
    tk.Label(root, text="La localisation est elle correcte? (O / N)").pack(pady=5)
    combo_geocodage_bon = tk.ttk.Combobox(root, values=["Oui", "Non"])
    combo_geocodage_bon.set("Oui")
    combo_geocodage_bon.pack(pady=5)
    root.title("Entrez les coordonnées si non correcte:")
    root.geometry("400x500")
    # Latitude
    tk.Label(root, text="Latitude:").pack(pady=5)
    entry_latitude = tk.Entry(root)
    entry_latitude.pack(pady=5)
    # Longitude
    tk.Label(root, text="Longitude:").pack(pady=5)
    entry_longitude = tk.Entry(root)
    entry_longitude.pack(pady=5)

    choix = geocodage_bon
    if choix == 'Non':
        # Création de l'interface graphique
        #root = tk.Tk()
        # root.title("Entrez les coordonnées:")
        # root.geometry("400x500")


        longitude = entry_longitude.get()
        latitude = entry_latitude.get()
        return longitude, latitude

    else:
        return lon, lat

