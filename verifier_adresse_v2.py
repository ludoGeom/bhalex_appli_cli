import geocodage
import tkinter as tk
from tkinter import messagebox, ttk
from geocodage_v2 import open_google_maps

def verif_adresse(adresse):
    """
    Vérifie l'adresse et retourne ses coordonnées géographiques

    Args:
        adresse (str): L'adresse complète à vérifier

    Returns:
        tuple: (longitude, latitude) ou None en cas d'erreur
    """
    # Appel à la fonction de geocodage
    lon, lat = geocodage.geocode_address(adresse)

    # Ouverture Google Maps
    open_google_maps(lon, lat)
    if lon is None or lat is None:
        print("⚠️ Adresse introuvable !")
        return None, None
    else:
        print(f"📍 Coordonnées obtenues : {lat}, {lon}")

    # Création d'une nouvelle fenêtre pour la vérification
    verification_window = tk.Toplevel()
    verification_window.title("Situation de l'adresse")
    verification_window.geometry("400x500")

    resultat = {'longitude': lon, 'latitude': lat}

    def valider_coordonnees():
        if combo_geocodage_bon.get() == "Non":
            try:
                resultat['longitude'] = float(entry_longitude.get())
                resultat['latitude'] = float(entry_latitude.get())
                return resultat['longitude'], resultat['latitude']
            except ValueError:
                messagebox.showerror("Erreur", "Les coordonnées doivent être des nombres valides")
                return

        else:
            return resultat['longitude'], resultat['latitude']

    #verification_window.destroy()
    # Interface de vérification
    tk.Label(verification_window, text="La localisation est-elle correcte?").pack(pady=5)
    combo_geocodage_bon = ttk.Combobox(verification_window, values=["Oui", "Non"])
    combo_geocodage_bon.set("Oui")
    combo_geocodage_bon.pack(pady=5)

    # Champs pour les coordonnées manuelles
    tk.Label(verification_window, text="Latitude:").pack(pady=5)
    entry_latitude = tk.Entry(verification_window)
    entry_latitude.insert(0, str(lat))
    entry_latitude.pack(pady=5)

    tk.Label(verification_window, text="Longitude:").pack(pady=5)
    entry_longitude = tk.Entry(verification_window)
    entry_longitude.insert(0, str(lon))
    entry_longitude.pack(pady=5)

    # Bouton de validation
    tk.Button(verification_window, text="Valider", command=valider_coordonnees).pack(pady=10)

    # Attendre que la fenêtre soit fermée
    verification_window.wait_window()


