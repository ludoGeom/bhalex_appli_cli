import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

# Connexion à la base de données
DB_CONFIG = {
    'dbname': 'commerce_db',
    'user': 'postgres',
    'password': 'password123',
    'host': 'localhost',
    'port': '5432'
}


# Fonction pour insérer un client, produit et un tarif avec géocodage
def inserer_client_produit_tarif():
    nom_client = entry_nom_client.get()
    adresse_client = entry_adresse_client.get()
    nom_produit = entry_nom_produit.get()
    description_produit = entry_description_produit.get()
    prix_tarif = entry_prix.get()
    date_tarif = entry_date.get()

    if not (nom_client and adresse_client and nom_produit and description_produit and prix_tarif and date_tarif):
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Géocodage de l'adresse
        cur.execute(
            """
            SELECT ST_AsText(ST_GeomFromText('POINT(' || x || ' ' || y || ')', 4326)) 
            FROM geocodage WHERE adresse = %s;
            """,
            (adresse_client,)
        )
        point_geom = cur.fetchone()

        if not point_geom:
            messagebox.showerror("Erreur", "Adresse non trouvée dans la base de géocodage")
            return

        # Insertion dans la table client
        cur.execute(
            """
            INSERT INTO client (nom, adresse, geom) 
            VALUES (%s, %s, ST_GeomFromText(%s, 4326)) RETURNING id;
            """,
            (nom_client, adresse_client, point_geom[0])
        )
        client_id = cur.fetchone()[0]

        # Insertion dans la table produit
        cur.execute(
            """
            INSERT INTO produit (nom, description, client_id) 
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (nom_produit, description_produit, client_id)
        )
        produit_id = cur.fetchone()[0]

        # Insertion dans la table tarif
        cur.execute(
            """
            INSERT INTO tarif (produit_id, prix, date_tarification) 
            VALUES (%s, %s, %s);
            """,
            (produit_id, prix_tarif, date_tarif)
        )

        conn.commit()
        messagebox.showinfo("Succès", "Client, produit et tarif ajoutés avec succès")
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


# Création de l'interface graphique
root = tk.Tk()
root.title("Gestion des Clients, Produits et Tarifs")
root.geometry("400x500")

# Champs d'entrée pour client, produit et tarif
tk.Label(root, text="Nom du client:").pack(pady=5)
entry_nom_client = tk.Entry(root)
entry_nom_client.pack(pady=5)

tk.Label(root, text="Adresse du client:").pack(pady=5)
entry_adresse_client = tk.Entry(root)
entry_adresse_client.pack(pady=5)

tk.Label(root, text="Nom du produit:").pack(pady=5)
entry_nom_produit = tk.Entry(root)
entry_nom_produit.pack(pady=5)

tk.Label(root, text="Description du produit:").pack(pady=5)
entry_description_produit = tk.Entry(root)
entry_description_produit.pack(pady=5)

tk.Label(root, text="Prix du tarif:").pack(pady=5)
entry_prix = tk.Entry(root)
entry_prix.pack(pady=5)

tk.Label(root, text="Date de tarification (YYYY-MM-DD):").pack(pady=5)
entry_date = tk.Entry(root)
entry_date.pack(pady=5)

# Bouton pour valider l'insertion
tk.Button(root, text="Ajouter Client, Produit et Tarif", command=inserer_client_produit_tarif).pack(pady=20)

root.mainloop()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
