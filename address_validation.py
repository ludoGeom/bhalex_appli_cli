
import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from geocodage_v2 import open_google_maps
import geocodage
import verifier_adresse_v2 as va

def valid():

    longitude, latitude = va.verif_adresse("5 rue emile blemont, 75018, paris")




if __name__ == '__main__':
    valid()
