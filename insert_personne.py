#!/usr/bin/env python3
# -*- coding : utf8 -*-

import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from psycopg2 import sql


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
    def inserer_personne_tel():
        nom_pers = entry_nom_pers.get()
        prenom_pers = entry_prenom_pers.get()
        genre_pers = combo_genre_pers.get()
        date_naiss = entry_date_naiss_pers.get()
        num_tel = entry_num_tel.get()
        type_tel = combo_type_tel.get()
        type_rue = entry_type_rue.get()
        num_rue = entry_num_rue.get()
        complement_num = entry_complement_num.get()
        nom_rue = entry_nom_rue.get()
        num_bati = entry_num_bati.get()
        hall = entry_hall.get()
        num_appart = entry_num_appart.get()
        code_postal = entry_code_postal.get()
        commune = entry_commune.get()
        adrs_principale = combo_adrs_principale.get()



        if not (nom_pers  and prenom_pers  and genre_pers and num_tel and type_tel):
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

            # Insertion dans la table telephone
            cur.execute(
                """
                INSERT INTO v1.telephone (numero, type_tel, personne_id)
                VALUES (%s, %s, %s) ;
                """,
                (num_tel, type_tel, id_personne)
            )

            # Insertion dans la table tel_personne
            cur.execute(
                """
                INSERT INTO v1.tel_personne (telephone_id, personne_id)
                VALUES (%s, %s) ;
                """,
                (num_tel, id_personne)
            )

            # Insertion dans la table adresse
            cur.execute(
                """
                INSERT INTO v1.adresse (type_rue , num_rue, complement_num, nom_rue, num_bati, hall, num_appart, code_postal, commune)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_adresse;
                """,
                (type_rue , num_rue, complement_num, nom_rue, num_bati, hall, num_appart, code_postal, commune)
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
    combo_genre_pers.pack(pady=5)

    tk.Label(root, text="Date de naissance de la personne:").pack(pady=5)
    entry_date_naiss_pers = tk.Entry(root)
    entry_date_naiss_pers.pack(pady=5)

    tk.Label(root, text="Numéro de téléphone:").pack(pady=5)
    entry_num_tel = tk.Entry(root)
    entry_num_tel.pack(pady=5)

    tk.Label(root, text="Type de téléphone: (perso / pro)").pack(pady=5)
    combo_type_tel = ttk.Combobox(root, values=["perso", "pro"])
    combo_type_tel.pack(pady=5)

    # Création de l'interface graphique
    root = tk.Tk()
    root.title("Gestion de l'adresse")
    root.geometry("400x500")

    tk.Label(root, text="Adresse principale ?").pack(pady=5)
    combo_adrs_principale = ttk.Combobox(root, values=["true", "false"])
    combo_adrs_principale.set("true")
    combo_adrs_principale.pack(pady=5)

    tk.Label(root, text="Type de rue:").pack(pady=5)
    entry_type_rue = tk.Entry(root)
    entry_type_rue.pack(pady=5)

    tk.Label(root, text="Intitulé de la rue:").pack(pady=5)
    entry_nom_rue = tk.Entry(root)
    entry_nom_rue.pack(pady=5)

    tk.Label(root, text="Numéro:").pack(pady=5)
    entry_num_rue = tk.Entry(root)
    entry_num_rue.pack(pady=5)

    tk.Label(root, text="Complément du numéro:").pack(pady=5)
    entry_complement_num  = tk.Entry(root)
    entry_complement_num.pack(pady=5)

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
    tk.Button(root, text="Ajouter la personne", command=inserer_personne_tel).pack(pady=20)

    root.mainloop()


#
# Fonction pour insérer un client, produit et un tarif avec géocodage
# def inserer_client_produit_tarif():
#     nom_client = entry_nom_client.get()
#     adresse_client = entry_adresse_client.get()
#     nom_produit = entry_nom_produit.get()
#     description_produit = entry_description_produit.get()
#     prix_tarif = entry_prix.get()
#     date_tarif = entry_date.get()
#
#     if not (nom_client and adresse_client and nom_produit and description_produit and prix_tarif and date_tarif):
#         messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
#         return
#
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cur = conn.cursor()
#
#         # Géocodage de l'adresse
#         cur.execute(
#             """
#             SELECT ST_AsText(ST_GeomFromText('POINT(' || x || ' ' || y || ')', 4326))
#             FROM geocodage WHERE adresse = %s;
#             """,
#             (adresse_client,)
#         )
#         point_geom = cur.fetchone()
#
#         if not point_geom:
#             messagebox.showerror("Erreur", "Adresse non trouvée dans la base de géocodage")
#             return
#
#         # Insertion dans la table client
#         cur.execute(
#             """
#             INSERT INTO client (nom, adresse, geom)
#             VALUES (%s, %s, ST_GeomFromText(%s, 4326)) RETURNING id;
#             """,
#             (nom_client, adresse_client, point_geom[0])
#         )
#         client_id = cur.fetchone()[0]
#
#         # Insertion dans la table produit
#         cur.execute(
#             """
#             INSERT INTO produit (nom, description, client_id)
#             VALUES (%s, %s, %s) RETURNING id;
#             """,
#             (nom_produit, description_produit, client_id)
#         )
#         produit_id = cur.fetchone()[0]
#
#         # Insertion dans la table tarif
#         cur.execute(
#             """
#             INSERT INTO tarif (produit_id, prix, date_tarification)
#             VALUES (%s, %s, %s);
#             """,
#             (produit_id, prix_tarif, date_tarif)
#         )
#
#         conn.commit()
#         messagebox.showinfo("Succès", "Client, produit et tarif ajoutés avec succès")
#         cur.close()
#         conn.close()
#
#     except Exception as e:
#         messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
#
#
# # Création de l'interface graphique
# root = tk.Tk()
# root.title("Gestion des Clients, Produits et Tarifs")
# root.geometry("400x500")
#
# # Champs d'entrée pour client, produit et tarif
# tk.Label(root, text="Nom du client:").pack(pady=5)
# entry_nom_client = tk.Entry(root)
# entry_nom_client.pack(pady=5)
#
# tk.Label(root, text="Adresse du client:").pack(pady=5)
# entry_adresse_client = tk.Entry(root)
# entry_adresse_client.pack(pady=5)
#
# tk.Label(root, text="Nom du produit:").pack(pady=5)
# entry_nom_produit = tk.Entry(root)
# entry_nom_produit.pack(pady=5)
#
# tk.Label(root, text="Description du produit:").pack(pady=5)
# entry_description_produit = tk.Entry(root)
# entry_description_produit.pack(pady=5)
#
# tk.Label(root, text="Prix du tarif:").pack(pady=5)
# entry_prix = tk.Entry(root)
# entry_prix.pack(pady=5)
#
# tk.Label(root, text="Date de tarification (YYYY-MM-DD):").pack(pady=5)
# entry_date = tk.Entry(root)
# entry_date.pack(pady=5)
#
# # Bouton pour valider l'insertion
# tk.Button(root, text="Ajouter Client, Produit et Tarif", command=inserer_client_produit_tarif).pack(pady=20)
#
# root.mainloop()
#
#

#

#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    connexion()
