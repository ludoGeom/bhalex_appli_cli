#!/usr/bin/env python3
# -*- coding : utf8 -*-
"""
Ce script a pour but d'entrer dans la base de nouveaux clients

"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "ludoinform@gmail.com"
__copyright__ = "Bhalex"
__credits__ = []
__date__ = "2025/05/05"
__deprecated__ = False
__email__ = "Ludoinform@gmail.com"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.03.1"


import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from geocodage_v2 import open_google_maps
import geocodage
import verifier_adresse_v3 as va


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
    root = tk.Tk()
    root.title("Gestion des personnes et adresses")
    root.geometry("500x600")  # Taille fixe pour la fenêtre

    # Création du notebook (gestionnaire d'onglets)
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    # Création des onglets
    tab_personne = ttk.Frame(notebook)
    tab_adresse = ttk.Frame(notebook)
    tab_validation = ttk.Frame(notebook)

    # Ajout des onglets au notebook
    notebook.add(tab_personne, text='Informations Personnelles')
    notebook.add(tab_adresse, text='Adresse')
    notebook.add(tab_validation, text='Validation')

    # --- Onglet Informations Personnelles ---
    fields_personne = [
        ("Nom:", "entry_nom_pers"),
        ("Prénom:", "entry_prenom_pers"),
        ("Date de naissance:", "entry_date_naiss_pers"),
        ("Numéro de téléphone:", "entry_num_tel")
    ]

    # Créer un dictionnaire pour stocker les références aux widgets
    entry_widgets = {}

    # Modifier la création des champs pour les stocker dans le dictionnaire
    for i, (label, var_name) in enumerate(fields_personne):
        ttk.Label(tab_personne, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="e")
        entry_widgets[var_name] = ttk.Entry(tab_personne)
        entry_widgets[var_name].grid(row=i, column=1, pady=5, padx=5, sticky="w")

    # Combobox pour le genre
    ttk.Label(tab_personne, text="Genre:").grid(row=len(fields_personne), column=0, pady=5, padx=5, sticky="e")
    combo_genre_pers = ttk.Combobox(tab_personne, values=["masculin", "feminin", "non-binaire"])
    combo_genre_pers.set("feminin")
    combo_genre_pers.grid(row=len(fields_personne), column=1, pady=5, padx=5, sticky="w")

    # Champ pour le numéro de téléphone
    ttk.Label(tab_personne, text="Numéro de téléphone:").grid(row=len(fields_personne), column=2, pady=5, padx=5, sticky="e")
    entry_num_tel = ttk.Entry(tab_personne)
    entry_num_tel.grid(row=len(fields_personne), column=3, pady=5, padx=5, sticky="w")

    # Combobox pour le type de téléphone
    ttk.Label(tab_personne, text="Type de téléphone:").grid(row=len(fields_personne) + 1, column=0, pady=5, padx=5,
                                                            sticky="e")
    combo_type_tel = ttk.Combobox(tab_personne, values=["perso", "pro"])
    combo_type_tel.set("perso")
    combo_type_tel.grid(row=len(fields_personne) + 1, column=1, pady=5, padx=5, sticky="w")





    # --- Onglet Adresse ---
    fields_adresse = [
        ("Numéro:", "entry_num_rue"),
        ("Complément:", "entry_complement_num"),
        ("Type de rue:", "entry_type_rue"),
        ("Article:", "entry_article_rue"),
        ("Nom de rue:", "entry_nom_rue"),
        ("Numéro bâtiment:", "entry_num_bati"),
        ("Hall:", "entry_hall"),
        ("Numéro appartement:", "entry_num_appart"),
        ("Code postal:", "entry_code_postal"),
        ("Commune:", "entry_commune")
    ]
    valeur_defaut = ["1", "", "rue","", "Championnet", "","","" , "75018", "Paris"]
    for i, (label, var_name) in enumerate(fields_adresse):
        ttk.Label(tab_adresse, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="e")
        entry_widgets[var_name] = ttk.Entry(tab_adresse)
        entry_widgets[var_name].insert(0, valeur_defaut[i])
        entry_widgets[var_name].grid(row=i, column=1, pady=5, padx=5, sticky="w")

    # Combobox pour adresse principale
    ttk.Label(tab_adresse, text="Adresse principale:").grid(row=len(fields_adresse), column=0, pady=5, padx=5,
                                                            sticky="e")
    combo_adrs_principale = ttk.Combobox(tab_adresse, values=["true", "false"])
    combo_adrs_principale.set("true")
    combo_adrs_principale.grid(row=len(fields_adresse), column=1, pady=5, padx=5, sticky="w")

    # Combobox pour aidant
    ttk.Label(tab_personne, text="Aidant:").grid(row=len(fields_personne) + 2, column=0, pady=5, padx=5, sticky="e")
    combo_aidant = ttk.Combobox(tab_personne, values=["true", "false"])
    combo_aidant.set("false")
    combo_aidant.grid(row=len(fields_personne) + 2, column=1, pady=5, padx=5, sticky="w")

    # --- Onglet Validation ---
    def get_form_data(entry_nom_pers=None):
        try:
            # Vérification du nom (champ obligatoire)
            if not entry_nom_pers.get():
                messagebox.showwarning("Champs manquants", "Le nom est obligatoire")
                notebook.select(0)  # Retour à l'onglet personne
                return
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cur = conn.cursor()

                #Insertion dans la table personne
                nom_pers = entry_nom_pers.get()
                prenom_pers = entry_widgets["entry_prenom_pers"].get()
                genre_pers = combo_genre_pers.get()
                date_naiss = entry_widgets["entry_date_naiss_pers"].get()
                num_tel = entry_num_tel.get()
                type_tel = combo_type_tel.get()
                type_rue = entry_widgets["entry_type_rue"].get()
                num_rue = entry_widgets["entry_num_rue"].get()
                complement_num = entry_widgets["entry_complement_num"].get()
                article_rue = entry_widgets["entry_article_rue"].get()
                nom_rue = entry_widgets["entry_nom_rue"].get()
                num_bati = entry_widgets["entry_num_bati"].get()
                hall = entry_widgets["entry_hall"].get()
                num_appart = entry_widgets["entry_num_appart"].get()
                code_postal = entry_widgets["entry_code_postal"].get()
                commune = entry_widgets["entry_commune"].get()
                adrs_principale = combo_adrs_principale.get()
                aidant = combo_aidant.get()
                #

                if date_naiss:
                    cur.execute(
                        """
                        INSERT INTO v1.personne (nom_pers, prenom, genre, date_naissance, aidant)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id_personne;
                        """,
                        (nom_pers, prenom_pers, genre_pers, date_naiss, aidant)
                    )
                    id_personne = cur.fetchone()[0]
                else:
                    cur.execute(
                        """
                        INSERT INTO v1.personne (nom_pers, prenom, genre, aidant)
                        VALUES (%s, %s, %s, %s) RETURNING id_personne;
                        """,
                        (nom_pers, prenom_pers, genre_pers, aidant)
                    )
                    id_personne = cur.fetchone()[0]


                # Insertion dans la table telephone
                cur.execute(
                    """
                    INSERT INTO v1.telephone (numero, type_tel)
                    VALUES (%s, %s) RETURNING id_telephone ;
                    """,
                    (num_tel, type_tel)
                )
                id_telephone = cur.fetchone()[0]

                # Insertion dans la table tel_personne
                cur.execute(
                    """
                    INSERT INTO v1.tel_personne (telephone_id, personne_id)
                    VALUES (%s, %s) ;
                    """,
                    (id_telephone , id_personne)
                )

                address = str(num_rue) + " " + complement_num + " " + type_rue + " " + article_rue + " " + nom_rue + ", "  +  code_postal  + " " +commune + ", France"
                print(address)

                # Appel à la fonction
                lon, lat = va.verif_adresse(address)

                # Insertion dans la table adresse
                cur.execute(
                    """
                    INSERT INTO v1.adresse (type_rue , num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal, commune, geom)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, public.ST_SetSRID(public.ST_Point(%s::double precision, %s::double precision), 4326)) RETURNING id_adresse;
                    """,
                    (type_rue, num_rue, complement_num, article_rue, nom_rue, num_bati, hall, num_appart, code_postal,
                     commune,float(lon), float(lat))

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
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
            try:
                conn.commit()
                messagebox.showinfo("Succès", "Personne ajoutée avec succès")
                cur.close()
                conn.close()

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


    def verify_address():
        # Construction de l'adresse complète
        address_parts = [
            entry_widgets['entry_num_rue'].get(), ", ",
            entry_widgets['entry_complement_num'].get(),
            entry_widgets['entry_type_rue'].get(),
            entry_widgets['entry_article_rue'].get(),
            entry_widgets['entry_nom_rue'].get(), ", ",
            entry_widgets['entry_code_postal'].get(), ", ",
            entry_widgets['entry_commune'].get(),
            "France"
        ]

        address = " ".join(filter(None, address_parts))
        print(address)
        try:
            # Vérification de l'adresse
            coordinates = va.verif_adresse(address)
            if coordinates:
                lon, lat = coordinates
                messagebox.showinfo("Vérification", f"Coordonnées vérifiées \nLongitude: {lon}\nLatitude: {lat}")
            else:
                messagebox.showerror("Erreur", "Impossible de vérifier l'adresse")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la vérification : {str(e)}")
        return address
    # Boutons de validation
    ttk.Button(tab_validation, text="Vérifier l'adresse", command= verify_address).pack(pady=20)
    ttk.Button(tab_validation, text="Valider et enregistrer", command=get_form_data).pack(pady=20)

    # Résumé des informations
    ttk.Label(tab_validation, text="Résumé des informations:").pack(pady=20)
    resume_text = tk.Text(tab_validation, height=10, width=40)
    resume_text.pack(pady=10, padx=10)

    def update_resume(event=None):
        resume_text.delete(1.0, tk.END)
        resume = f"""Nom: {entry_widgets['entry_nom_pers'].get()}
    Prénom: {entry_widgets['entry_prenom_pers'].get()}
    Genre: {combo_genre_pers.get()}
    Téléphone: {entry_widgets['entry_num_tel'].get()}

    Adresse:
    {entry_widgets['entry_num_rue'].get()} {entry_widgets['entry_type_rue'].get()} {entry_widgets['entry_nom_rue'].get()}
    {entry_widgets['entry_code_postal'].get()} {entry_widgets['entry_commune'].get()}
    """
        resume_text.insert(1.0, resume)


    # Mise à jour du résumé lors du changement d'onglet
    notebook.bind('<<NotebookTabChanged>>', update_resume)

    root.mainloop()


#get_form_data()
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
