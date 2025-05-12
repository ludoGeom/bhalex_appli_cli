#!/usr/bin/env python3
# -*- coding : utf8 -*-
"""
Ce script a pour but d'entrer dans la base de nouveaux clients

"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "Ludovic.BOUTIGNON@plainecommune.fr"
__copyright__ = "Bhalex"
__credits__ = []
__date__ = "2025/05/01"
__deprecated__ = False
__email__ = "Ludoinform@gmail.com"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.03.0"


import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from geocodage_v2 import open_google_maps
import geocodage
import verifier_adresse as va


def connexion(nom_pers=None, geocodage_bon=None, address=None):

    # Connexion à la base de données
    DB_CONFIG = {
        'dbname': 'sap',
        'user': 'ludo',
        'password': 'test',
        'host': 'localhost',
        'port': '5432',
        'options' : '-c search_path=v1'
    }
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Gestion des personnes et adresses")

    # Création des frames
    frame_personne = tk.Frame(root)
    frame_personne.pack(pady=10, padx=10, fill="x")

    frame_adresse = tk.Frame(root)
    frame_adresse.pack(pady=10, padx=10, fill="x")

    # Création des widgets
    # Variables globales pour les widgets
    tk.Label(frame_personne, text="Nom:").pack()
    entry_nom_pers = tk.Entry(frame_personne)
    entry_nom_pers.pack()

    tk.Label(frame_personne, text="Prénom:").pack()
    entry_prenom_pers = tk.Entry(frame_personne)
    entry_prenom_pers.pack()

    tk.Label(frame_personne, text="Genre:").pack()
    combo_genre_pers = ttk.Combobox(frame_personne, values=["masculin", "feminin", "non-binaire"])
    combo_genre_pers.set("feminin")
    combo_genre_pers.pack()

    tk.Label(frame_personne, text="Date de naissance:").pack()
    entry_date_naiss_pers = tk.Entry(frame_personne)
    entry_date_naiss_pers.pack()

    tk.Label(frame_personne, text="Téléphone:").pack()
    entry_num_tel = tk.Entry(frame_personne)
    entry_num_tel.pack()

    tk.Label(frame_personne, text="Type de téléphone:").pack()
    combo_type_tel = ttk.Combobox(frame_personne, values=["perso", "pro"])
    combo_type_tel.set("perso")
    combo_type_tel.pack()

    tk.Label(frame_adresse, text="Adresse principale:").pack()
    combo_adrs_principale = ttk.Combobox(frame_adresse, values=["true", "false"])
    combo_adrs_principale.set("true")
    combo_adrs_principale.pack()

    tk.Label(root, text="Numéro:").pack(pady=5)
    entry_num_rue = tk.Entry(root)
    entry_num_rue.pack(pady=5)

    tk.Label(root, text="Complément du numéro:").pack(pady=5)
    entry_complement_num = tk.Entry(root)
    entry_complement_num.pack(pady=5)

    tk.Label(root, text="Type de rue:").pack(pady=5)
    entry_type_rue = tk.Entry(root)
    # entry_type_rue.set("rue")
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
    entry_hall = tk.Entry(root)
    entry_hall.pack(pady=5)

    tk.Label(root, text="Numéro d'appartement:").pack(pady=5)
    entry_num_appart = tk.Entry(root)
    entry_num_appart.pack(pady=5)

    tk.Label(root, text="Code postal:").pack(pady=5)
    entry_code_postal = tk.Entry(root)
    entry_code_postal.pack(pady=5)

    tk.Label(root, text="Commune:").pack(pady=5)
    entry_commune = tk.Entry(root)
    # entry_commune.set("Paris")  # Valeur par défaut
    entry_commune.pack(pady=5)


    # fonction pour récupérer les données du formulaire
    def get_form_data():

        nom_pers = entry_nom_pers.get()
        prenom_pers = entry_prenom_pers.get()
        genre_pers = combo_genre_pers.get()
        date_naiss = entry_date_naiss_pers.get()
        num_tel = entry_num_tel.get()
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

        if not nom_pers:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
            return

        try:
            # Votre code d'insertion dans la base de données reste le même
            # ...
            messagebox.showinfo("Succès", "Personne ajoutée avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")



        def get_adrs(num_rue, complement_num, type_rue, article_rue, nom_rue , code_postal ,commune ):
            return str(num_rue) + " " + complement_num + " " + type_rue + " " + article_rue + " " + nom_rue + ", " + code_postal + " " + commune + ", France"

        #print(get_adrs(num_rue, complement_num, type_rue, article_rue, nom_rue , code_postal ,commune ))

        # tk.Label(root, text="L'adresse est elle correcte? (O / N)").pack(pady=5)
        # combo_geocodage_bon = ttk.Combobox(root, values=["Oui", "Non"])
        # combo_geocodage_bon.set("Oui")
        # combo_geocodage_bon.pack(pady=5)



    # Bouton pour valider
    tk.Button(root, text="Valider", command=get_form_data).pack(pady=20)

    # Bouton pour vérifier l'adresse
    #tk.Button(root, text="Vérifier l'adresse", command=va.verif_adresse(address)).pack(pady=20)

    # Bouton pour valider l'insertion
    #tk.Button(root, text="Ajouter la personne", command=inserer_personne).pack(pady=20)

    root.mainloop()

    get_form_data()
    # #Fonction pour insérer une personne dans la base
    # def inserer_personne(lon=None, lat=None):
    #     nom_pers = entry_nom_pers.get()
    #     prenom_pers = entry_prenom_pers.get()
    #     genre_pers = combo_genre_pers.get()
    #     date_naiss = entry_date_naiss_pers.get()
    #     num_tel = entry_num_tel.get()
    #     type_tel = combo_type_tel.get()
    #     type_rue = entry_type_rue.get()
    #     num_rue = entry_num_rue.get()
    #     complement_num = entry_complement_num.get()
    #     article_rue = entry_article_rue.get()
    #     nom_rue = entry_nom_rue.get()
    #     num_bati = entry_num_bati.get()
    #     hall = entry_hall.get()
    #     num_appart = entry_num_appart.get()
    #     code_postal = entry_code_postal.get()
    #     commune = entry_commune.get()
    #     adrs_principale = combo_adrs_principale.get()
    #     aidant = combo_aidant.get()
    #
    #
    #
    #
    #     #  if not (nom_pers and prenom_pers  and genre_pers and num_tel and type_tel)
    #     if not (nom_pers):
    #         messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
    #         return
    #
    #     try:
    #         conn = psycopg2.connect(**DB_CONFIG)
    #         cur = conn.cursor()
    #
    #         #Insertion dans la table personne
    #         if date_naiss:
    #             cur.execute(
    #                 """
    #                 INSERT INTO v1.personne (nom_pers, prenom, genre, date_naissance, aidant)
    #                 VALUES (%s, %s, %s, %s, %s) RETURNING id_personne;
    #                 """,
    #                 (nom_pers, prenom_pers, genre_pers, date_naiss, aidant)
    #             )
    #             id_personne = cur.fetchone()[0]
    #         else:
    #             cur.execute(
    #                 """
    #                 INSERT INTO v1.personne (nom_pers, prenom, genre, aidant)
    #                 VALUES (%s, %s, %s, %s, %s) RETURNING id_personne;
    #                 """,
    #                 (nom_pers, prenom_pers, genre_pers, aidant)
    #             )
    #             id_personne = cur.fetchone()[0]
    #
    #
    #         # Insertion dans la table telephone
    #         cur.execute(
    #             """
    #             INSERT INTO v1.telephone (numero, type_tel)
    #             VALUES (%s, %s) RETURNING id_telephone ;
    #             """,
    #             (num_tel, type_tel)
    #         )
    #         id_telephone = cur.fetchone()[0]
    #
    #         # Insertion dans la table tel_personne
    #         cur.execute(
    #             """
    #             INSERT INTO v1.tel_personne (telephone_id, personne_id)
    #             VALUES (%s, %s) ;
    #             """,
    #             (id_telephone , id_personne)
    #         )
    #
    #         address = str(num_rue) + " " + complement_num + " " + type_rue + " " + article_rue + " " + nom_rue + ", "  +  code_postal  + " " +commune + ", France"
    #         print(address)
    #
    #         # Appel à la fonction
    #         #lon, lat = va.verif_adresse(address)
    #
    #         # Insertion dans la table adresse
    #         cur.execute(
    #             """
    #             INSERT INTO v1.adresse (type_rue , num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal, commune, geom)
    #             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, public.ST_SetSRID(public.ST_Point(%s::double precision, %s::double precision), 4326)) RETURNING id_adresse;
    #             """,
    #             (type_rue, num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal,
    #              commune,float(lon), float(lat))
    #
    #         )
    #         id_adresse = cur.fetchone()[0]
    #
    #         # Insertion dans la table localisation
    #         cur.execute(
    #             """
    #             INSERT INTO v1.localisation (adrs_principale, personne_id, adresse_id)
    #             VALUES (%s, %s, %s) ;
    #             """,
    #             (adrs_principale, id_personne, id_adresse)
    #         )
    #
    #         conn.commit()
    #         messagebox.showinfo("Succès", "Personne ajoutée avec succès")
    #         cur.close()
    #         conn.close()
    #
    #     except Exception as e:
    #         messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
    #



if __name__ == '__main__':
    connexion()
