#!/usr/bin/env python3
# -*- coding : utf8 -*-
"""
Ce script a pour but d'entrer dans la base de nouveaux clients ou aidants
ce script intègre la version insert_personne_v3_3.py et l'intègre dans un processus d'application rassemblant les différents programmes:
insertion, modification de personne et adhésion

"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "ludoinform@gmail.com"
__copyright__ = "Bhalex"
__credits__ = []
__date__ = "2025/06/02"
__deprecated__ = False
__email__ = "Ludoinform@gmail.com"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.03.3"
"""
v0.03.3: Ajout de la table adhesion
"""

import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import verifier_adresse_v3 as va

def create_app(parent):
    print("App1 lancée")
    # Crée une fenêtre fille (Toplevel) liée à la fenêtre parente
    top = tk.Toplevel(parent)
    top.title("Application Insérer personne")

    # notebook = ttk.Notebook(top)
    # notebook.pack(pady=10, expand=True)

    # Ajoute le contenu de l'application
    label = tk.Label(top, text="Insérer une personne dans la base de données")
    label.pack(padx=20, pady=40)


    def connexion(nom_pers=None, geocodage_bon=None, address=None):
        global validated_coordinates
        validated_coordinates = {'lon': None, 'lat': None}

        # Connexion à la base de données
        DB_CONFIG = {
            'dbname': 'sap',
            'user': 'ludo',
            'password': 'test',
            'host': 'localhost',
            'port': '5432',
            'options': '-c search_path=v1'
        }
        # root = tk.Tk()
        #top = tk.Toplevel(parent)
        top.title("Gestion des personnes et adresses")
        top.geometry("500x600")  # Taille fixe pour la fenêtre
        top.configure(bg="#96c0eb")

        # Création du notebook (gestionnaire d'onglets)
        notebook = ttk.Notebook(top)
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
            ("Numéro de téléphone:", "entry_num_tel"),
            ("Date d'adhesion:", "entry_date_adhesion"),
            ("Montant payé:", "entry_prix_paye_ad")
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
        combo_genre_pers = ttk.Combobox(tab_personne, values=["Masculin", "Féminin", "Non-binaire"])
        combo_genre_pers.set("Féminin")
        combo_genre_pers.grid(row=len(fields_personne), column=1, pady=5, padx=5, sticky="w")

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
        valeur_defaut = ["1", "", "rue", "", "Championnet", "", "", "", "75018", "Paris"]
        for i, (label, var_name) in enumerate(fields_adresse):
            ttk.Label(tab_adresse, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="e")
            entry_widgets[var_name] = ttk.Entry(tab_adresse)
            entry_widgets[var_name].insert(0, valeur_defaut[i])
            entry_widgets[var_name].grid(row=i, column=1, pady=5, padx=5, sticky="w")

        # Combobox pour adresse principale
        ttk.Label(tab_adresse, text="Adresse principale:").grid(row=len(fields_adresse), column=0, pady=5, padx=5,
                                                                sticky="e")
        combo_adrs_principale = ttk.Combobox(tab_adresse, values=["Oui", "Non"])
        combo_adrs_principale.set("Oui")
        combo_adrs_principale.grid(row=len(fields_adresse), column=1, pady=5, padx=5, sticky="w")

        # Combobox pour aidant
        ttk.Label(tab_personne, text="Aidant potentiel:").grid(row=len(fields_personne) + 2, column=0, pady=5, padx=5,
                                                               sticky="e")
        combo_aidant = ttk.Combobox(tab_personne, values=["Oui", "Non", "Peut-être"])
        combo_aidant.set("Non")
        combo_aidant.grid(row=len(fields_personne) + 2, column=1, pady=5, padx=5, sticky="w")

        # --- Onglet Validation ---
        def get_form_data():
            try:
                # Vérifier si l'adresse a été validée
                if validated_coordinates['lon'] is None or validated_coordinates['lat'] is None:
                    messagebox.showerror("Erreur", "Veuillez d'abord vérifier l'adresse")
                    return

                # Récupération des données du formulaire avec vérification
                data = {}

                # Onglet Personne
                nom_pers = entry_widgets["entry_nom_pers"].get().strip()
                if not nom_pers:
                    messagebox.showwarning("Champs manquants", "Le nom est obligatoire")
                    notebook.select(0)  # Retour à l'onglet personne
                    return

                # Récupération des autres champs
                num_rue = entry_widgets['entry_num_rue'].get().strip()
                type_rue = entry_widgets['entry_type_rue'].get().strip()
                nom_rue = entry_widgets['entry_nom_rue'].get().strip()
                code_postal = entry_widgets['entry_code_postal'].get().strip()
                commune = entry_widgets['entry_commune'].get().strip()

                # Vérification des champs obligatoires de l'adresse
                if not all([num_rue, type_rue, nom_rue, code_postal, commune]):
                    messagebox.showwarning("Champs manquants",
                                           "Tous les champs obligatoires de l'adresse doivent être remplis")
                    return

                try:
                    print("Tentative de connexion à la base de données...")
                    conn = psycopg2.connect(**DB_CONFIG)
                    cur = conn.cursor()

                    # Début de la transaction
                    print("Début de la transaction...")

                    # Insertion de l'adresse
                    print("Insertion de l'adresse...")
                    cur.execute(
                        """
                        INSERT INTO v1.adresse ( type_rue, num_rue, complement_num, article_rue, nom_rue, 
                                              num_bati, hall, num_appart, code_postal, commune, geom)
                        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                               public.ST_SetSRID(public.ST_MakePoint(%s::double precision, %s::double precision), 4326))
                        RETURNING id_adresse;
                        """,

                        (type_rue, num_rue,
                         entry_widgets['entry_complement_num'].get().strip(),
                         entry_widgets['entry_article_rue'].get().strip(),
                         nom_rue,
                         entry_widgets['entry_num_bati'].get().strip(),
                         entry_widgets['entry_hall'].get().strip(),
                         entry_widgets['entry_num_appart'].get().strip(),
                         code_postal, commune,
                         validated_coordinates['lon'], validated_coordinates['lat'])
                    )

                    id_adresse = cur.fetchone()[0]
                    print(f"Adresse insérée avec succès, id: {id_adresse}")

                    # Insertion dans la table personne
                    nom_pers = entry_widgets["entry_nom_pers"].get()
                    prenom_pers = entry_widgets["entry_prenom_pers"].get()
                    genre_pers = combo_genre_pers.get()
                    date_naiss = entry_widgets["entry_date_naiss_pers"].get()
                    num_tel = entry_widgets["entry_num_tel"].get()
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
                    aidant = combo_aidant.get()
                    adrs_principale = combo_adrs_principale.get()
                    date_adhesion = entry_widgets["entry_date_adhesion"].get()
                    prix_paye_ad = entry_widgets["entry_prix_paye_ad"].get()

                    if adrs_principale == "Oui":
                        adrs_principale = True
                    else:
                        adrs_principale = False

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
                        print(f"Personne insérée avec succès, id: {id_personne}")

                    #  Insertion du telephone
                    if num_tel:
                        # Insertion dans la table telephone
                        cur.execute(
                            """
                            INSERT INTO v1.telephone (numero, type_tel)
                            VALUES (%s, %s) RETURNING id_telephone ;
                            """,
                            (entry_widgets['entry_num_tel'].get(), type_tel)
                        )
                        id_telephone = cur.fetchone()[0]

                        # Insertion dans la table tel_personne
                        cur.execute(
                            """
                            INSERT INTO v1.tel_personne (telephone_id, personne_id)
                            VALUES (%s, %s) ;
                            """,
                            (id_telephone, id_personne)
                        )

                    # Insertion dans la table localisation
                    cur.execute(
                        """
                        INSERT INTO v1.localisation (adrs_principale, personne_id, adresse_id)
                        VALUES (%s, %s, %s) ;
                        """,
                        (adrs_principale, id_personne, id_adresse)
                    )

                    # Insertion dans la table adhesion
                    if date_adhesion:
                        if prix_paye_ad:
                            cur.execute(
                                """
                                INSERT INTO v1.adhesion (date_adhesion, prix_paye,personne_id)
                                VALUES (%s, %s, %s) ;
                                """,
                                (date_adhesion, prix_paye_ad, id_personne)
                            )
                            id_adhesion = cur.fetchone()[0]
                        else:
                            cur.execute(
                                """
                                INSERT INTO v1.adhesion (date_adhesion, prix_paye,personne_id)
                                VALUES (%s, %s, %s) ;
                                """,
                                (date_adhesion, 0.0, id_personne)
                            )
                            id_adhesion = cur.fetchone()[0]
                except Exception as e:
                    messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
                try:
                    conn.commit()
                    messagebox.showinfo("Succès", "Personne ajoutée avec succès")
                    # Réinitialisation du formulaire
                    # for widget in entry_widgets.values():
                    #     widget.delete(0, tk.END)
                    # combo_genre_pers.set('')
                    # combo_type_tel.set('')
                    # combo_adrs_principale.set('')
                    # combo_aidant.set('')
                    # resume_text.delete(1.0, tk.END)

                except psycopg2.Error as e:
                    conn.rollback()
                    print(f"Erreur PostgreSQL : {e.pgerror}")
                    messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données :\n{str(e)}")
                except Exception as e:
                    conn.rollback()
                    print(f"Erreur générale : {str(e)}")
                    messagebox.showerror("Erreur", f"Erreur lors de l'insertion : {str(e)}")
                finally:
                    if 'cur' in locals():
                        cur.close()
                    if 'conn' in locals():
                        conn.close()
                    print("Connexion fermée")

            except Exception as e:
                print(f"Erreur dans get_form_data : {str(e)}")
                messagebox.showerror("Erreur", f"Erreur générale : {str(e)}")

        validated_coordinates = {'lon': None, 'lat': None}

        def verify_address():
            try:
                # Construction de l'adresse complète
                num_rue = entry_widgets['entry_num_rue'].get().strip()
                type_rue = entry_widgets['entry_type_rue'].get().strip()
                nom_rue = entry_widgets['entry_nom_rue'].get().strip()
                code_postal = entry_widgets['entry_code_postal'].get().strip()
                commune = entry_widgets['entry_commune'].get().strip()

                address = f"{num_rue} {type_rue} {nom_rue}, {code_postal} {commune}, France"
                address = ' '.join(address.split())
                print(f"Adresse à vérifier : {address}")

                coordinates = va.verif_adresse(address)
                if coordinates:
                    lon, lat = coordinates
                    # Stocker les coordonnées validées
                    validated_coordinates['lon'] = lon
                    validated_coordinates['lat'] = lat
                    messagebox.showinfo("Vérification",
                                        f"Adresse validée :\n{address}\n\n"
                                        f"Coordonnées :\nLongitude : {lon}\n"
                                        f"Latitude : {lat}")
                    return True
                else:
                    messagebox.showerror("Erreur",
                                         "Impossible de vérifier l'adresse.\n"
                                         "Veuillez vérifier que l'adresse est correcte.")
                    return False

            except Exception as e:
                messagebox.showerror("Erreur",
                                     f"Erreur lors de la vérification :\n{str(e)}")
                return False

        # Boutons de validation
        tk.Button(tab_validation, text="Vérifier l'adresse", command=verify_address, bg= "#fbca52", fg="white", activebackground="#ff0000").pack(pady=20)
        tk.Button(tab_validation, text="Valider et enregistrer", command=get_form_data, bg="#42d507", fg="white", activebackground="#42d507").pack(pady=20)

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
        Aidant: {combo_aidant.get()}

        Adresse:
        {entry_widgets['entry_num_rue'].get()} {entry_widgets['entry_type_rue'].get()} {entry_widgets['entry_nom_rue'].get()}
        {entry_widgets['entry_code_postal'].get()} {entry_widgets['entry_commune'].get()}
        """
            resume_text.insert(1.0, resume)

        # Mise à jour du résumé lors du changement d'onglet
        notebook.bind('<<NotebookTabChanged>>', update_resume)



    # if __name__ == '__main__':
    #     connexion()

    connexion()

    # bouton fermer
    btn_close = tk.Button(top, text="Fermer", command=top.destroy,  bg="#ff0000", fg="white", activebackground="#ff0000")
    btn_close.pack(pady=10)


#Permet de tester l'application indépendamment
# if __name__ == "__main__":
#     root= tk.Tk()
#     create_app(root)
#     root.mainloop()
