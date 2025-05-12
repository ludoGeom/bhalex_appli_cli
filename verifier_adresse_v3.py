import geocodage_v2 as geo
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
    lon, lat = geo.geocode_address(adresse)

    # Ouverture Google Maps
    open_google_maps(lon, lat)
    if lon is None or lat is None:
        messagebox.showerror("Erreur", "⚠️ Adresse introuvable !")
        return None

    print(f"📍 Coordonnées obtenues : {lat}, {lon}")

    # Création d'une nouvelle fenêtre pour la vérification
    verification_window = tk.Toplevel()
    verification_window.title("Vérification de l'adresse")
    verification_window.geometry("400x500")

    coordonnees_validees = {'validees': False, 'longitude': lon, 'latitude': lat}

    def on_choix_validation(event):
        if combo_geocodage_bon.get() == "Non":
            entry_latitude.config(state='normal')
            entry_longitude.config(state='normal')
        else:
            entry_latitude.config(state='disabled')
            entry_longitude.config(state='disabled')

    def valider_coordonnees():
        try:
            if combo_geocodage_bon.get() == "Non":
                coordonnees_validees['longitude'] = float(entry_longitude.get())
                coordonnees_validees['latitude'] = float(entry_latitude.get())
            else:
                coordonnees_validees['longitude'] = lon
                coordonnees_validees['latitude'] = lat

            coordonnees_validees['validees'] = True
            verification_window.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Les coordonnées doivent être des nombres valides")

    # Interface de vérification
    tk.Label(verification_window, text="La localisation est-elle correcte ?").pack(pady=10)
    combo_geocodage_bon = ttk.Combobox(verification_window, values=["Oui", "Non"], state="readonly")
    combo_geocodage_bon.set("Oui")
    combo_geocodage_bon.pack(pady=5)
    combo_geocodage_bon.bind('<<ComboboxSelected>>', on_choix_validation)

    # Champs pour les coordonnées
    tk.Label(verification_window, text="Latitude :").pack(pady=5)
    entry_latitude = tk.Entry(verification_window)
    entry_latitude.insert(0, str(lat))
    entry_latitude.config(state='disabled')
    entry_latitude.pack(pady=5)

    tk.Label(verification_window, text="Longitude :").pack(pady=5)
    entry_longitude = tk.Entry(verification_window)
    entry_longitude.insert(0, str(lon))
    entry_longitude.config(state='disabled')
    entry_longitude.pack(pady=5)

    # Bouton de validation
    tk.Button(verification_window, text="Valider", command=valider_coordonnees).pack(pady=20)

    # Attendre que la fenêtre soit fermée
    verification_window.wait_window()

    if coordonnees_validees['validees']:
        return (coordonnees_validees['longitude'], coordonnees_validees['latitude'])
    return None