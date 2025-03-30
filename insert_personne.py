#!/usr/bin/env python3
# -*- coding : utf8 -*-

"""
    Ce script A pour but d'entrer les caractéristiques des clients ou aidants de bhalex

    TODO:


"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "Ludovic.BOUTIGNON@plainecommune.fr"
__copyright__ = "ludoGeom"
__credits__ = []
__date__ = "2025/03/30"
__deprecated__ = False
__email__ = "Ludovic Boutignon"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.01.02"


import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from geocodage_v2 import open_google_maps
import geocodage
import carte_folium as cf

def connexion(nom_pers=None):

    # Connexion à la base de données
    DB_CONFIG = {
        'dbname': 'sap',
        'user': 'ludo',
        'password': 'test',
        'host': 'localhost',
        'port': '5432',
        'options' : '-c search_path=v1'
    }


    #Fonction pour insérer un client, produit et un tarif avec géocodage
    def inserer_personne_tel_adrs():
        nom_pers = entry_nom_pers.get()
        prenom_pers = entry_prenom_pers.get()
        genre_pers = combo_genre_pers.get()
        date_naiss = entry_date_naiss_pers.get()
        #num_tel = entry_num_tel.get()
        num_tel2 = entry_num_tel2.get()
        type_tel = combo_type_tel.get()
        type_rue = entry_type_rue.get()
        num_rue = entry_num_rue.get()
        complement_num = entry_complement_num.get()
        article_rue = entry_article_rue.get()
        nom_rue = entry_nom_rue.get()
        num_bati = entry_num_bati.get()
        hall = entry_hall.get()
        num_appart = entry_num_appart.get()
        code_postal = entry_code_postal.get()
        commune = entry_commune.get()
        adrs_principale = combo_adrs_principale.get()


        #  if not (nom_pers and prenom_pers  and genre_pers and num_tel and type_tel)
        if not (nom_pers  ):
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
            return

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            #Insertion dans la table client
            cur.execute(
                """
                INSERT INTO v1.personne (nom_pers, prenom, genre, date_naissance)
                VALUES (%s, %s, %s, %s) RETURNING id_personne;
                """,
                (nom_pers, prenom_pers, genre_pers, date_naiss)
            )
            id_personne = cur.fetchone()[0]

            # # Insertion dans la table telephone
            # cur.execute(
            #     """
            #     INSERT INTO v1.telephone (numero, type_tel, personne_id)
            #     VALUES (%s, %s, %s) ;
            #     """,
            #     (num_tel, type_tel, id_personne)
            # )

            # # Insertion dans la table tel_personne
            # cur.execute(
            #     """
            #     INSERT INTO v1.tel_personne (telephone_id, personne_id)
            #     VALUES (%s, %s) ;
            #     """,
            #     (num_tel, id_personne)
            # )

            # Insertion dans la table tel
            cur.execute(
                """
                INSERT INTO v1.tel (numero, type_tel, personne_id)
                VALUES (%s, %s, %s) ;
                """,
                (num_tel2, type_tel, id_personne)
            )

            # Insertion dans la table tel_pers
            cur.execute(
                """
                INSERT INTO v1.tel_pers (numero, personne_id)
                VALUES (%s, %s) ;
                """,
                (num_tel2, id_personne)
            )

            address = str(num_rue) + " " + complement_num + " " + type_rue + " " + article_rue + " " + nom_rue + ", "  +  code_postal  + " " +commune + ", France"
            print(address)

            # Appel à la fonction de geocodage
            lon, lat = geocodage.geocode_address(address)

            # Ouverture Google Maps
            open_google_maps(lon, lat)
            if lon is None or lat is None:
                print("⚠️ Adresse introuvable !")
            else:
                print(f"📍 Coordonnées obtenues : {lat}, {lon}")

            # Demander confirmation ou correction
            choix = input("Le point est-il correct ? (o/n) : ").strip().lower()
            if choix == 'n':
                lat = input("Entrez une nouvelle latitude : ")
                lon = input("Entrez une nouvelle longitude : ")

            # # Avec la carte folium
            # cf.carteFolium()


            # Insertion dans la table adresse
            cur.execute(
                """
                INSERT INTO v1.adresse (type_rue , num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal, commune, geom)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, public.ST_SetSRID(public.ST_Point(%s::double precision, %s::double precision), 4326)) RETURNING id_adresse;
                """,
                (type_rue , num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal, commune,  float(lon), float(lat))
            )
            id_adresse = cur.fetchone()[0]

            # Insertion dans la table localisation
            cur.execute(
                """
                INSERT INTO v1.localisation (adrs_principale, personne_id, adresse_id)
                VALUES (%s, %s, %s) ;
                """,
                (adrs_principale, id_personne, id_adresse)
            )

            conn.commit()
            messagebox.showinfo("Succès", "Personne ajoutée avec succès")
            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    # Création de l'interface graphique
    root = tk.Tk()
    root.title("Gestion des personnes")
    root.geometry("400x500")

    # Champs d'entrée pour personne
    tk.Label(root, text="Nom de la personne:").pack(pady=5)
    entry_nom_pers = tk.Entry(root)
    entry_nom_pers.pack(pady=5)

    tk.Label(root, text="Prénom de la personne:").pack(pady=5)
    entry_prenom_pers = tk.Entry(root)
    entry_prenom_pers.pack(pady=5)

    tk.Label(root, text="Genre de la personne:").pack(pady=5)
    combo_genre_pers = ttk.Combobox(root, values=["masculin", "feminin", "non-binaire"])
    combo_genre_pers.set("feminin")
    combo_genre_pers.pack(pady=5)

    tk.Label(root, text="Date de naissance de la personne:").pack(pady=5)
    entry_date_naiss_pers = tk.Entry(root)
    entry_date_naiss_pers.pack(pady=5)

    # tk.Label(root, text="Numéro de téléphone:").pack(pady=5)
    # entry_num_tel = tk.Entry(root)
    # #entry_num_tel.set("0612345678")
    # entry_num_tel.pack(pady=5)

    tk.Label(root, text="Numéro téléphonique:").pack(pady=5)
    entry_num_tel2 = tk.Entry(root)
    # entry_num_tel.set("0612345678")
    entry_num_tel2.pack(pady=5)

    tk.Label(root, text="Type de téléphone: (perso / pro)").pack(pady=5)
    combo_type_tel = ttk.Combobox(root, values=["perso", "pro"])
    combo_type_tel.set("perso")
    combo_type_tel.pack(pady=5)

    # Création de l'interface graphique
    root = tk.Tk()
    root.title("Gestion de l'adresse")
    root.geometry("400x900")

    tk.Label(root, text="Adresse principale ?").pack(pady=5)
    combo_adrs_principale = ttk.Combobox(root, values=["true", "false"])
    combo_adrs_principale.set("true")
    combo_adrs_principale.pack(pady=5)

    tk.Label(root, text="Numéro:").pack(pady=5)
    entry_num_rue = tk.Entry(root)
    entry_num_rue.pack(pady=5)

    tk.Label(root, text="Complément du numéro:").pack(pady=5)
    entry_complement_num = tk.Entry(root)
    entry_complement_num.pack(pady=5)

    tk.Label(root, text="Type de rue:").pack(pady=5)
    entry_type_rue = tk.Entry(root)
    #entry_type_rue.set("rue")
    entry_type_rue.pack(pady=5)

    tk.Label(root, text="Article (de/des...):").pack(pady=5)
    entry_article_rue = tk.Entry(root)
    entry_article_rue.pack(pady=5)

    tk.Label(root, text="Intitulé de la rue:").pack(pady=5)
    entry_nom_rue = tk.Entry(root)
    entry_nom_rue.pack(pady=5)

    tk.Label(root, text="Numéro de bâtiment:").pack(pady=5)
    entry_num_bati = tk.Entry(root)
    entry_num_bati.pack(pady=5)

    tk.Label(root, text="Hall:").pack(pady=5)
    entry_hall= tk.Entry(root)
    entry_hall.pack(pady=5)

    tk.Label(root, text="Numéro d'appartement:").pack(pady=5)
    entry_num_appart = tk.Entry(root)
    entry_num_appart.pack(pady=5)

    tk.Label(root, text="Code postal:").pack(pady=5)
    entry_code_postal  = tk.Entry(root)
    entry_code_postal.pack(pady=5)

    tk.Label(root, text="Commune:").pack(pady=5)
    entry_commune = tk.Entry(root)
    #entry_commune.set("Paris")  # Valeur par défaut
    entry_commune.pack(pady=5)


    # Bouton pour valider l'insertion
    tk.Button(root, text="Ajouter la personne", command=inserer_personne_tel_adrs).pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    connexion()
