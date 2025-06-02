#!/usr/bin/env python3
# -*- coding : utf8 -*-
"""
Ce script a pour but de modifier les données d'une personne il intègre le script modif_personne_v1.py
"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "ludoinform@gmail.com"
__copyright__ = "Bhalex"
__credits__ = []
__date__ = "2025/05/18"
__deprecated__ = False
__email__ = "ludoinform@gmail.com"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.00.1"



import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import verifier_adresse_v3 as va
from geocodage_v2 import open_google_maps

def create_app(parent):
    print("App2 lancée")
    # Crée une fenêtre fille (Toplevel) liée à la fenêtre parente
    top = tk.Toplevel(parent)
    top.title("Application Modifier personne")

    # notebook = ttk.Notebook(top)
    # notebook.pack(pady=10, expand=True)

    # Ajoute le contenu de l'application
    label = tk.Label(top, text="Modifier une personne")
    label.pack(padx=20, pady=20)

    def open_google_maps(url):
        """Ouvre l'URL dans le navigateur par défaut"""
        import webbrowser
        webbrowser.open(url)

    def connexion(nom_pers=None):
        # Connexion à la base de données
        DB_CONFIG = {
            'dbname': 'sap',
            'user': 'ludo',
            'password': 'test',
            'host': 'localhost',
            'port': '5432',
            'options': '-c search_path=v1'
        }

        try:
            return psycopg2.connect(**DB_CONFIG)
        except Exception as e:
            messagebox.showerror("Erreur de connexion", f"Échec de la connexion : {e}")
            return None

    class Application(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Recherche de Personnes")
            self.geometry("1200x600")

            # Configuration du style
            self.style = ttk.Style()
            self.style.configure("Treeview", rowheight=25)

            self.create_widgets()

        def create_widgets(self):
            # Frame de recherche
            search_frame = ttk.Frame(self)
            search_frame.pack(pady=10, fill=tk.X)

            ttk.Label(search_frame, text="Nom de famille :").pack(side=tk.LEFT, padx=5)
            self.nom_entry = ttk.Entry(search_frame, width=30)
            self.nom_entry.pack(side=tk.LEFT, padx=5)

            search_btn = ttk.Button(search_frame, text="Rechercher", command=self.execute_search)
            search_btn.pack(side=tk.LEFT, padx=5)

            # Treeview avec scrollbars
            self.tree_frame = ttk.Frame(self)
            self.tree_frame.pack(expand=True, fill=tk.BOTH)

            self.tree = ttk.Treeview(self.tree_frame, columns=(
                "id_personne", "Prénom", "Nom", "Naissance", "Genre", "Aidant",
                "Téléphone", "Type tel", "Numéro", "Complément", "type_rue", "Article",
                "Rue", "Appartement", "Bati", "Hall", "Code Postal", "Commune"
            ), show="headings")
            self.tree.heading("id_personne", text="id_personne")
            vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
            hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            self.tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")

            self.tree_frame.grid_rowconfigure(0, weight=1)
            self.tree_frame.grid_columnconfigure(0, weight=1)

            # Configuration des colonnes
            headers = [("Identifiant", 100),
                       ("Prénom", 100), ("Nom", 120), ("Naissance", 100),
                       ("Genre", 60), ("Aidant", 80), ("Téléphone", 100), ("Type tel", 60),
                       ("Numéro", 80), ("Complément", 100), ("Type de voie", 60), ("Article", 80),
                       ("Rue", 150), ("Appartement", 100), ("N° Bati", 60), ("Hall", 60), ("Code Postal", 90),
                       ("Commune", 120)
                       ]
            edit_btn = ttk.Button(self, text="Modifier la sélection", command=self.edit_selected)
            edit_btn.pack(pady=5)

            for idx, (text, width) in enumerate(headers):
                self.tree.heading(f"#{idx + 1}", text=text)
                self.tree.column(f"#{idx + 1}", width=width, anchor=tk.W)

        def execute_search(self):
            nom = self.nom_entry.get().strip()
            if not nom:
                messagebox.showwarning("Champ vide", "Veuillez saisir un nom de famille")
                return

            conn = connexion()
            if not conn:
                return

            try:
                with conn.cursor() as cur:
                    query = """
                        SELECT id_personne, prenom, nom_pers, date_naissance, genre, aidant, 
                               t.numero, t.type_tel, ad.num_rue, ad.complement_num, ad.type_rue, ad.article_rue, 
                               ad.nom_rue, ad.num_appart, ad.num_bati, ad.hall, ad.code_postal, ad.commune
                        FROM v1.personne
                        LEFT JOIN v1.localisation AS l ON l.personne_id = id_personne
                        LEFT JOIN v1.adresse AS ad ON ad.id_adresse = l.adresse_id
                        LEFT JOIN v1.tel_personne AS tp ON tp.personne_id = id_personne
                        LEFT JOIN v1.telephone AS t ON t.id_telephone = tp.telephone_id
                        WHERE nom_pers = %s
                                    """
                    cur.execute(query, (nom,))
                    rows = cur.fetchall()

                    # Nettoyer le Treeview
                    self.tree.delete(*self.tree.get_children())

                    if not rows:
                        messagebox.showinfo("Aucun résultat", f"Aucune personne trouvée pour le nom '{nom}'")
                        return

                    # Formater les données pour le Treeview
                    for row in rows:
                        formatted_row = [
                            row[0],  # id_personne
                            str(row[1]) if row[1] else "",  # prénom
                            str(row[2]) if row[2] else "",  # nom_pers
                            row[3].strftime("%d/%m/%Y") if row[3] else "",  # date_naissance
                            str(row[4]).capitalize() if row[4] else "",  # genre
                            row[5] if row[5] else "",  # aidant ("Oui", "Non", "Peut-être")
                            self.format_phone(row[6]) if row[6] else "",  # téléphone
                            str(row[7]) if row[7] else "perso",  # type_tel
                            str(row[8]) if row[8] else "",  # num_rue
                            str(row[9]) if row[9] else "",  # complement_num
                            str(row[10]) if row[10] else "",  # type_rue
                            str(row[11]) if row[11] else "",  # article_rue
                            str(row[12]) if row[12] else "",  # nom_rue
                            str(row[13]) if row[13] else "",  # num_appart
                            str(row[14]) if row[14] else "",  # num_bati
                            str(row[15]) if row[15] else "",  # hall
                            str(row[16]) if row[16] else "",  # code_postal
                            str(row[17]) if row[17] else ""  # commune
                        ]
                        self.tree.insert("", tk.END, values=formatted_row)

            except psycopg2.Error as e:
                messagebox.showerror("Erreur SQL", f"Erreur lors de l'exécution de la requête :\n{str(e)}")
            finally:
                if conn:
                    conn.close()

        def format_phone(self, number):
            """Formate les numéros de téléphone français"""
            num = str(number)
            if len(num) == 10:
                return f"{num[0:2]} {num[2:4]} {num[4:6]} {num[6:8]} {num[8:10]}"
            return num

        def edit_selected(self):
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne à modifier.")
                return
            values = self.tree.item(selected, "values")
            EditWindow(self, values)

        def update_person(self, id_personne, new_values):
            # new_values
            # indices:
            # 0: Prénom, 1: Nom, 2: Naissance, 3: Genre, 4: Aidant, etc.
            conn = connexion()
            if not conn:
                return
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                                   UPDATE v1.personne
                                   SET prenom=%s, nom_pers=%s, date_naissance=%s, genre=%s, aidant=%s
                                   WHERE id_personne=%s
                               """, (
                        new_values[0],  # Prénom
                        new_values[1],  # Nom
                        self.convert_date(new_values[2]),  # Naissance
                        new_values[3],  # Genre
                        new_values[4],  # Aidant
                        id_personne  # WHERE id_personne=...
                    ))
                    # Gestion du numéro de téléphone
                    telephone = new_values[5].replace(" ", "")  # Supprime les espaces
                    type_tel = new_values[6]  # Type de téléphone (personnel/professionnel)

                    if telephone:  # Si un numéro est fourni
                        # Vérifie si un téléphone existe déjà pour cette personne
                        cur.execute("""
                                        SELECT t.id_telephone, t.numero, t.type_tel

                                        FROM v1.tel_personne tp
                                        JOIN v1.telephone t ON t.id_telephone = tp.telephone_id
                                        WHERE tp.personne_id = %s
                                    """, (id_personne,))
                        tel_existant = cur.fetchone()

                        if tel_existant:
                            # Mise à jour du numéro existant
                            cur.execute("""
                                            UPDATE v1.telephone 
                                            SET numero = %s , type_tel = %s
                                            WHERE id_telephone = %s
                                        """, (telephone, type_tel, tel_existant[0]))
                        else:
                            # Création d'un nouveau numéro
                            cur.execute("""
                                            INSERT INTO v1.telephone (numero, type_tel)
                                            VALUES (%s, %s)
                                            RETURNING id_telephone
                        """,
                                        (telephone, type_tel))
                            nouveau_tel_id = cur.fetchone()[0]

                            # Création du lien avec la personne
                            cur.execute("""
                                            INSERT INTO v1.tel_personne (personne_id, telephone_id)
                                            VALUES (%s, %s)
                                        """, (id_personne, nouveau_tel_id))

                    # Met à jour les autres tables selon la logique de ton modèle
                    # Exemples :
                    # cur.execute("UPDATE v1.telephone SET numero=%s WHERE ...", (new_values[5], ...))
                    # cur.execute("UPDATE v1.adresse SET num_rue=%s, ... WHERE ...", (...))
                    # À adapter selon ta clé primaire réelle et tes besoins

                conn.commit()
                messagebox.showinfo("Succès", "Modification enregistrée.")
                self.execute_search()  # Rafraîchir l’affichage
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
            finally:
                conn.close()

        def convert_date(self, date_str):
            """Convertit une date JJ/MM/AAAA en AAAA-MM-JJ pour PostgreSQL"""
            from datetime import datetime
            try:
                return datetime.strptime(date_str, "%d/%m/%Y").date()
            except:
                return None

        def update_address(self, personne_id, new_values):
            conn = connexion()
            if not conn:
                return
            try:
                with conn.cursor() as cur:
                    # Recherche de l'adresse liée à la personne
                    cur.execute("""
                        SELECT adresse_id 
                        FROM v1.localisation 
                        WHERE personne_id = %s
                    """, (personne_id,))
                    adresse_id = cur.fetchone()
                    if adresse_id:
                        adresse_id = adresse_id[0]
                        # Mise à jour de l'adresse
                        cur.execute("""
                            UPDATE v1.adresse SET
                                num_rue = %s,
                                complement_num = %s,
                                type_rue = %s,
                                article_rue = %s,
                                nom_rue = %s,
                                num_appart = %s,
                                num_bati = %s,
                                hall = %s,
                                code_postal = %s,
                                commune = %s
                            WHERE id_adresse = %s
                        """, (
                            new_values[0], new_values[1], new_values[2], new_values[3], new_values[4],
                            new_values[5], new_values[6], new_values[7], new_values[8], new_values[9],
                            adresse_id
                        ))
                    else:
                        # Création d'une nouvelle adresse
                        cur.execute("""
                            INSERT INTO v1.adresse
                            (num_rue, complement_num, type_rue, article_rue, nom_rue,
                             num_appart, num_bati, hall, code_postal, commune)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id_adresse
                        """, (
                            new_values[0], new_values[1], new_values[2], new_values[3], new_values[4],
                            new_values[5], new_values[6], new_values[7], new_values[8], new_values[9]
                        ))
                        adresse_id = cur.fetchone()[0]
                        # Création du lien localisation
                        cur.execute("""
                            INSERT INTO v1.localisation (personne_id, adresse_id)
                            VALUES (%s, %s)
                        """, (personne_id, adresse_id))
                    conn.commit()
                    self.execute_search()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour de l'adresse : {e}")
            finally:
                conn.close()

    class AddressEditWindow(tk.Toplevel):
        def __init__(self, parent, personne_id, current_values, callback):
            super().__init__(parent)
            self.title("Modifier l'adresse")
            self.parent = parent
            self.personne_id = personne_id
            self.callback = callback
            self.current_values = current_values
            self.verified = False
            self.coordinates = None

            # Frame principale
            main_frame = ttk.Frame(self)
            main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Frame pour les champs d'adresse
            address_frame = ttk.LabelFrame(main_frame, text="Adresse")
            address_frame.pack(fill=tk.X, padx=5, pady=5)

            labels = [
                "Numéro rue", "Complément numéro", "Type rue", "Article rue", "Nom rue",
                "Numéro appartement", "Numéro bâtiment", "Hall", "Code postal", "Commune"
            ]
            self.entries = []

            # Champs de saisie
            for i, label in enumerate(labels):
                tk.Label(address_frame, text=label).grid(row=i, column=0, sticky="e", padx=5)
                entry = tk.Entry(address_frame, width=40)
                entry.grid(row=i, column=1, padx=5, pady=2)
                if current_values and i < len(current_values):
                    # Nettoyage de la valeur avant insertion
                    cleaned_value = ""
                    if current_values[i] is not None:
                        cleaned_value = str(current_values[i]).strip()
                        if cleaned_value.isspace():  # Vérifie si la chaîne ne contient que des espaces
                            cleaned_value = ""
                    entry.insert(0, cleaned_value)
                self.entries.append(entry)

            # Frame pour les boutons
            self.button_frame = ttk.Frame(main_frame)
            self.button_frame.pack(fill=tk.X, padx=5, pady=10)

            # Bouton de vérification
            self.verify_btn = ttk.Button(self.button_frame, text="Vérifier l'adresse",
                                         command=self.verify_address)
            self.verify_btn.pack(side=tk.LEFT, padx=5)

            # Bouton de sauvegarde (initialement désactivé)
            self.save_btn = ttk.Button(self.button_frame, text="Enregistrer",
                                       command=self.save, state='disabled')
            self.save_btn.pack(side=tk.LEFT, padx=5)

            # Label pour le statut
            self.status_label = ttk.Label(main_frame, text="")
            self.status_label.pack(fill=tk.X, padx=5)

            # Frame pour les boutons Oui/Non (créer après les autres frames)
            self.yn_frame = ttk.LabelFrame(main_frame,
                                           text="Vérification de l'adresse")  # Changement ici : main_frame au lieu de self

            # Label de question
            self.question_label = ttk.Label(self.yn_frame, text="La localisation est-elle correcte ?")
            self.question_label.pack(side=tk.TOP, pady=5)

            # Frame pour contenir les boutons côte à côte
            button_container = ttk.Frame(self.yn_frame)
            button_container.pack(side=tk.TOP, pady=5)

            # Bouton Oui
            self.yes_btn = ttk.Button(button_container, text="Oui",
                                      command=self.on_yes_click)
            self.yes_btn.pack(side=tk.LEFT, padx=5)

            # Bouton Non
            self.no_btn = ttk.Button(button_container, text="Non",
                                     command=self.on_no_click)
            self.no_btn.pack(side=tk.LEFT, padx=5)

        def on_yes_click(self):
            print("Bouton Oui cliqué")
            self.answer_location(True)

        def on_no_click(self):
            print("Bouton Non cliqué")
            self.answer_location(False)

        def verify_address(self):
            print("Début de verify_address")
            try:
                # Récupération des champs nécessaires
                num_rue = self.entries[0].get().strip()
                type_rue = self.entries[2].get().strip()
                nom_rue = self.entries[4].get().strip()
                code_postal = self.entries[8].get().strip()
                commune = self.entries[9].get().strip()

                # Construction de l'adresse complète
                address = f"{num_rue} {type_rue} {nom_rue}, {code_postal} {commune}, France"
                address = ' '.join(address.split())
                print(f"Adresse à vérifier : {address}")

                # Vérification de l'adresse
                coordinates = va.verif_adresse(address)

                if coordinates:
                    lon, lat = coordinates
                    self.coordinates = {'lon': lon, 'lat': lat}

                    # Ouvrir Google Maps
                    url = f"https://www.google.com/maps?q={lat},{lon}"
                    open_google_maps(url)

                    print("Tentative d'affichage des boutons Oui/Non")

                    # Cacher d'abord le frame s'il est déjà affiché
                    self.yn_frame.pack_forget()

                    # Réafficher le frame
                    self.yn_frame.pack(pady=10)

                    print("État du yn_frame :")
                    print(f"- Visible : {self.yn_frame.winfo_ismapped()}")
                    print(f"- Géométrie : {self.yn_frame.winfo_geometry()}")

                    self.status_label.config(
                        text="Veuillez vérifier la localisation sur la carte",
                        foreground="black"
                    )

                    # Forcer la mise à jour
                    self.update()

                    return True
                else:
                    self.status_label.config(
                        text="Impossible de vérifier l'adresse",
                        foreground="red"
                    )
                    return False

            except Exception as e:
                print(f"Erreur dans verify_address : {str(e)}")
                self.status_label.config(
                    text=f"Erreur : {str(e)}",
                    foreground="red"
                )
                return False

        def answer_location(self, is_correct):
            print(f"answer_location appelé avec {is_correct}")  # Debug
            if is_correct:
                self.verified = True
                self.save_btn.config(state='normal')
                self.status_label.config(
                    text="Adresse vérifiée avec succès",
                    foreground="green"
                )
            else:
                self.verified = False
                self.save_btn.config(state='disabled')
                self.status_label.config(
                    text="Veuillez corriger l'adresse et réessayer",
                    foreground="red"
                )
            self.yn_frame.pack_forget()

        def save(self):
            if not self.verified:
                return

            new_values = [entry.get() for entry in self.entries]

            if hasattr(self, 'coordinates') and self.coordinates:
                new_values.extend([str(self.coordinates['lon']), str(self.coordinates['lat'])])

            if self.callback:
                self.callback(self.personne_id, self.current_values, new_values)

            self.destroy()

    class EditWindow(tk.Toplevel):
        def __init__(self, parent, values):
            super().__init__(parent)
            self.title("Modifier la personne")
            self.parent = parent
            self.values = values
            self.entries = []
            labels = [
                "Identifiant", "Prénom", "Nom", "Naissance (JJ/MM/AAAA)", "Genre", "Aidant (Oui/Non/Peut-être)",
                "Numéro de téléphone", "Type de téléphone"

            ]
            for i, label in enumerate(labels):
                tk.Label(self, text=label).grid(row=i, column=0, sticky="e")
                if i == 0:
                    # Champ ID en lecture seule
                    entry = tk.Entry(self, width=40, state="readonly")
                    entry.grid(row=i, column=1, padx=5, pady=2)
                    entry.insert(0, values[0])
                elif label.startswith("Aidant"):
                    self.aidant_var = tk.StringVar()
                    self.aidant_combo = ttk.Combobox(
                        self, textvariable=self.aidant_var,
                        values=["Oui", "Non", "Peut-être"], state="readonly"
                    )
                    self.aidant_combo.grid(row=i, column=1, padx=5, pady=2)
                    self.aidant_combo.set(values[i])
                    self.entries.append(self.aidant_combo)
                elif label.startswith("Genre"):
                    self.genre_var = tk.StringVar()
                    self.genre_combo = ttk.Combobox(
                        self, textvariable=self.genre_var,
                        values=["Masculin", "Féminin", "Non-binaire"], state="readonly"
                    )
                    self.genre_combo.grid(row=i, column=1, padx=5, pady=2)
                    self.genre_combo.set(values[i])
                    self.entries.append(self.genre_combo)
                elif label.startswith("Type de téléphone"):
                    self.type_tel_var = tk.StringVar()
                    self.type_tel_combo = ttk.Combobox(
                        self, textvariable=self.type_tel_var,
                        values=["perso", "pro"], state="readonly",
                        width=37

                    )
                    self.type_tel_combo.grid(row=i, column=1, padx=5, pady=2)
                    # Si une valeur existe déjà, on la sélectionne
                    if len(values) > i and values[i]:
                        self.type_tel_combo.set(values[i])
                    else:
                        self.type_tel_combo.set("perso")  # Valeur par défaut
                    self.entries.append(self.type_tel_combo)



                else:
                    entry = tk.Entry(self, width=40)
                    entry.grid(row=i, column=1, padx=5, pady=2)
                    entry.insert(0, values[i])
                    self.entries.append(entry)
            save_btn = tk.Button(self, text="Enregistrer", command=self.save)
            save_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)
            addr_btn = tk.Button(self, text="Modifier l'adresse",
                                 command=lambda: self.open_address_edit(self.values[0],
                                                                        self.values[8:] if len(
                                                                            self.values) > 8 else [""] * 10))
            addr_btn.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

        def open_address_edit(self, personne_id, current_values):
            # Assurer qu'on a une liste de 10 éléments
            address_values = list(current_values)
            while len(address_values) < 10:
                address_values.append("")

            # Limiter à 10 éléments si on en a plus
            address_values = address_values[:10]

            # Maintenant on peut accéder aux indices en toute sécurité
            formatted_values = [
                address_values[0],  # num_rue
                address_values[1],  # complement_num
                address_values[2],  # type_rue
                address_values[3],  # article_rue
                address_values[4],  # nom_rue
                address_values[5],  # num_appart
                address_values[6],  # num_bati
                address_values[7],  # hall
                address_values[8],  # code_postal
                address_values[9]  # commune
            ]

            # Définir une fonction de callback
            def on_address_update(personne_id, _, new_values):
                # Vous pouvez ajouter ici la logique de mise à jour nécessaire
                self.parent.update_address(personne_id, new_values)

            AddressEditWindow(self, personne_id, current_values, callback=on_address_update)

        def save(self):
            # Récupérer les valeurs modifiées (hors ID)
            new_values = [e.get() for e in self.entries]
            self.parent.update_person(self.values[0], new_values)  # ID, puis les champs modifiables
            self.destroy()

    # if __name__ == "__main__":
    #     app = Application()
    #     app.mainloop()
    Application()

    # bouton fermer
    btn_close = tk.Button(top, text="Fermer", command=top.destroy)
    btn_close.pack(pady=10)

#Permet de tester l'application indépendamment
# if __name__ == "__main__":
#     root= tk.Tk()
#     create_app(root)
#     root.mainloop()