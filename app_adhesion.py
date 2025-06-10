#!/usr/bin/env python3
# -*- coding : utf8 -*-
"""
Ce script a pour but d'acter une adhesion il se base sur le script adhesion_v1.py
"""

__author__ = "Ludovic Boutignon"
__authors__ = ["Ludovic Boutignon"]
__contact__ = "ludoinform@gmail.com"
__copyright__ = "Bhalex"
__credits__ = []
__date__ = "2025/05/25"
__deprecated__ = False
__email__ = "Ludoinform@gmail.com"
__license__ = "GPL"
__maintainer__ = "Ludovic Boutignon"
__status__ = "Production en cours"
__version__ = "0.00.1"

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import psycopg2


def create_app(parent):
    print("App3 lancée")
    # Crée une fenêtre fille (Toplevel) liée à la fenêtre parente
    #top = tk.Toplevel(parent)
    #top.title("Application Acter une adhésion")

    # notebook = ttk.Notebook(top)
    # notebook.pack(pady=10, expand=True)

    # Ajoute le contenu de l'application
    #label = tk.Label(top, text="Données d'adhésion")
    #label.pack(padx=20, pady=20)
    #top.configure(bg="#96c0eb")


    def connexion():
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
            self.title("Gestion des adhésions")
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

            search_btn = tk.Button(search_frame, text="Rechercher", command=self.execute_search,  bg="#fbca52", fg="white", activebackground="blue")
            search_btn.pack(side=tk.LEFT, padx=5)

            # Treeview avec scrollbars
            self.tree_frame = ttk.Frame(self)
            self.tree_frame.pack(expand=True, fill=tk.BOTH)

            self.tree = ttk.Treeview(self.tree_frame, columns=(
                "id_personne", "Prénom", "Nom", "Naissance", "Genre", "Aidant",
                "Téléphone", "Type tel", "Date adhésion", "Prix payé", "Prix à payer"
            ), show="headings")

            # Configuration des colonnes
            headers = [
                ("id_personne", "Identifiant", 100),
                ("Prénom", "Prénom", 100),
                ("Nom", "Nom", 120),
                ("Naissance", "Naissance", 100),
                ("Genre", "Genre", 60),
                ("Aidant", "Aidant", 80),
                ("Téléphone", "Téléphone", 100),
                ("Type tel", "Type tel", 60),
                ("Date adhésion", "Date adhésion", 100),
                ("Prix payé", "Prix payé", 60),
                ("Prix à payer", "Prix à payer", 60)
            ]

            for id_col, text, width in headers:
                self.tree.heading(id_col, text=text)
                self.tree.column(id_col, width=width, anchor=tk.W)

            # Scrollbars
            vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
            hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            # Placement des éléments avec grid
            self.tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")

            self.tree_frame.grid_rowconfigure(0, weight=1)
            self.tree_frame.grid_columnconfigure(0, weight=1)

            # Bouton de modification
            edit_btn = tk.Button(self, text="Modifier la sélection", command=self.edit_selected, bg= "#fbca52", fg="white", activebackground="#ff0000")
            edit_btn.pack(pady=5)

        def format_phone(self, number):
            """Formate les numéros de téléphone français"""
            if number:
                num = str(number)
                if len(num) == 10:
                    return f"{num[0:2]} {num[2:4]} {num[4:6]} {num[6:8]} {num[8:10]}"
            return ""

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
                        SELECT p.id_personne, p.prenom, p.nom_pers, p.date_naissance, p.genre, p.aidant, 
                               t.numero, t.type_tel, ad.date_adhesion, ad.prix_paye, 
                               (SELECT prix_tarif_ad
                                FROM v1.tarif_adhesion as ta
                                WHERE date_tarif_ad = (SELECT MAX(ta2.date_tarif_ad) FROM v1.tarif_adhesion as ta2)) as prix_a_payer
                        FROM v1.personne p
                        LEFT JOIN v1.localisation AS l ON l.personne_id = p.id_personne                  
                        LEFT JOIN v1.tel_personne AS tp ON tp.personne_id = p.id_personne
                        LEFT JOIN v1.telephone AS t ON t.id_telephone = tp.telephone_id
                        LEFT JOIN v1.adhesion AS ad ON ad.personne_id = p.id_personne
                        WHERE p.nom_pers = %s
                    """
                    cur.execute(query, (nom,))
                    rows = cur.fetchall()

                    # Nettoyer le Treeview
                    for item in self.tree.get_children():
                        self.tree.delete(item)

                    if not rows:
                        messagebox.showinfo("Aucun résultat", f"Aucune personne trouvée pour le nom '{nom}'")
                        return

                    # Afficher les résultats
                    for row in rows:
                        formatted_row = [
                            row[0],  # id_personne
                            str(row[1]) if row[1] else "",  # prénom
                            str(row[2]) if row[2] else "",  # nom_pers
                            row[3].strftime("%d/%m/%Y") if row[3] else "",  # date_naissance
                            str(row[4]).capitalize() if row[4] else "",  # genre
                            row[5] if row[5] else "",  # aidant
                            self.format_phone(row[6]) if row[6] else "",  # téléphone
                            str(row[7]) if row[7] else "perso",  # type_tel
                            row[8].strftime("%Y-%m-%d") if row[8] else "",  # date adhesion
                            str(row[9]) if row[9] else "",  # prix paye
                            str(row[10]) if row[10] else ""  # prix à payer
                        ]
                        self.tree.insert("", tk.END, values=formatted_row)

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")
            finally:
                conn.close()

        def edit_selected(self):
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne à modifier.")
                return
            values = self.tree.item(selected)["values"]
            EditWindow(self, values)

        def update_adhesion(self, id_personne, new_values):
            conn = connexion()
            if not conn:
                return
            try:
                with conn.cursor() as cur:
                    # D'abord, récupérons le dernier tarif d'adhésion
                    cur.execute("""
                        SELECT id_tarif_ad, prix_tarif_ad
                        FROM v1.tarif_adhesion as ta
                        WHERE date_tarif_ad = (
                            SELECT MAX(ta.date_tarif_ad) 
                            FROM v1.tarif_adhesion as ta
                        )
                    """)
                    tarif = cur.fetchone()
                    if not tarif:
                        messagebox.showerror("Erreur", "Aucun tarif d'adhésion trouvé")
                        return

                    id_tarif, prix_tarif = tarif

                    # Vérifions si une adhésion existe déjà pour cette personne
                    cur.execute("""
                        SELECT personne_id FROM v1.adhesion WHERE personne_id = %s
                    """, (id_personne,))

                    adhesion_existe = cur.fetchone()

                    if adhesion_existe:
                        # Si l'adhésion existe, on la met à jour
                        cur.execute("""
                            UPDATE v1.adhesion
                            SET date_adhesion = %s, 
                                prix_paye = %s,
                                tarif_ad_id = %s
                            WHERE personne_id = %s
                        """, (
                            new_values[0],  # date_adhesion
                            new_values[1],  # prix_paye
                            id_tarif,  # tarif_ad_id
                            id_personne
                        ))
                    else:
                        # Si l'adhésion n'existe pas, on la crée
                        cur.execute("""
                            INSERT INTO v1.adhesion (personne_id, date_adhesion, prix_paye, tarif_ad_id)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            id_personne,
                            new_values[0],  # date_adhesion
                            new_values[1],  # prix_paye
                            id_tarif  # tarif_ad_id
                        ))

                    conn.commit()
                    messagebox.showinfo("Succès",
                                        f"Modification de l'adhésion enregistrée.\nTarif à payer : {prix_tarif}€")
                    self.execute_search()  # Rafraîchir l'affichage

            except psycopg2.Error as e:
                conn.rollback()
                messagebox.showerror("Erreur SQL", f"Erreur lors de la mise à jour : {str(e)}")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
            finally:
                conn.close()

    class EditWindow(tk.Toplevel):
        def __init__(self, parent, values):
            super().__init__(parent)
            self.title("Modifier l'adhésion")
            self.parent = parent
            self.id_personne = values[0]

            # Frame principale
            main_frame = ttk.Frame(self, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Informations de la personne (en lecture seule)
            ttk.Label(main_frame, text="Prénom :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            prenom_entry = ttk.Entry(main_frame, width=30, state="readonly")
            prenom_entry.grid(row=0, column=1, padx=5, pady=5)
            prenom_entry.insert(0, values[1])

            ttk.Label(main_frame, text="Nom :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            nom_entry = ttk.Entry(main_frame, width=30, state="readonly")
            nom_entry.grid(row=1, column=1, padx=5, pady=5)
            nom_entry.insert(0, values[2])

            ttk.Label(main_frame, text="Téléphone :").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            tel_entry = ttk.Entry(main_frame, width=30, state="readonly")
            tel_entry.grid(row=2, column=1, padx=5, pady=5)
            tel_entry.insert(0, values[6] if values[6] else "")

            ttk.Label(main_frame, text="Genre :").grid(row=3, column=0, padx=5, pady=5, sticky="e")
            genre_entry = ttk.Entry(main_frame, width=30, state="readonly")
            genre_entry.grid(row=3, column=1, padx=5, pady=5)
            genre_entry.insert(0, values[4])

            ttk.Label(main_frame, text="Aidant :").grid(row=4, column=0, padx=5, pady=5, sticky="e")
            aidant_entry = ttk.Entry(main_frame, width=30, state="readonly")
            aidant_entry.grid(row=4, column=1, padx=5, pady=5)
            aidant_entry.insert(0, values[5])

            # Champs modifiables pour l'adhésion
            ttk.Label(main_frame, text="Date d'adhésion (JJ/MM/AAAA) :").grid(row=5, column=0, padx=5, pady=5,
                                                                              sticky="e")
            self.date_adhesion = ttk.Entry(main_frame, width=30)
            self.date_adhesion.grid(row=5, column=1, padx=5, pady=5)
            if values[8]:  # Date d'adhésion
                try:
                    date_obj = datetime.strptime(values[8], '%Y-%m-%d')
                    self.date_adhesion.insert(0, date_obj.strftime('%d/%m/%Y'))
                except ValueError:
                    self.date_adhesion.insert(0, values[8])

            ttk.Label(main_frame, text="Prix payé :").grid(row=6, column=0, padx=5, pady=5, sticky="e")
            self.prix_paye = ttk.Entry(main_frame, width=30)
            self.prix_paye.grid(row=6, column=1, padx=5, pady=5)
            self.prix_paye.insert(0, values[9] if values[9] else "")

            # Boutons
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

            tk.Button(btn_frame, text="Enregistrer", command=self.save, bg="#42d507", fg="white", activebackground="#42d507").pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Annuler", command=self.destroy, bg="#ff0000", fg="white", activebackground="#ff0000").pack(side=tk.LEFT, padx=5)

            # Rendre la fenêtre modale
            self.transient(parent)
            self.grab_set()

        def save(self):
            try:
                date_adhesion = self.date_adhesion.get().strip()
                prix_paye = self.prix_paye.get().strip()

                if not date_adhesion or not prix_paye:
                    messagebox.showerror("Erreur", "La date d'adhésion et le prix payé sont obligatoires")
                    return

                # Validation et conversion de la date du format français vers le format SQL
                try:
                    date_obj = datetime.strptime(date_adhesion, '%d/%m/%Y')
                    date_sql = date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ/MM/AAAA")
                    return

                # Validation du prix
                try:
                    prix = float(prix_paye)
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix doit être un nombre")
                    return

                # Appel de la méthode de mise à jour avec la date au format SQL
                self.parent.update_adhesion(self.id_personne, [date_sql, prix])
                self.destroy()

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    # if __name__ == "__main__":
    #     app = Application()
    #     app.mainloop()
    Application()

    # Exemple de bouton
    #btn_close = tk.Button(top, text="Fermer", command=top.destroy, bg="#ff0000", fg="white", activebackground="#ff0000")
    #btn_close.pack(pady=10)

if __name__ == "__main__":
    root= tk.Tk()
    create_app(root)
    root.mainloop()