"""
Dashboard des Températures Mondiales 2023

Ce script est l'application principale d'un dashboard interactif.
Son rôle est de :
1. Charger les données de températures mondiales depuis un fichier CSV.
2. Définir la structure visuelle de la page web (titres, textes, etc.).
3. Lancer un serveur web local pour afficher le dashboard dans un navigateur.

L'application est construite avec la bibliothèque Dash.
"""


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# --- 1. Lecture des données ---
# On lit le fichier CSV que notre script get_data.py a généré
try:
    df = pd.read_csv("data/raw/temperatures_2023.csv")
except FileNotFoundError:
    print("Erreur: Le fichier 'temperatures_2023.csv' est introuvable.")
    print("Assurez-vous d'avoir lancé le script 'get_data.py' avant de lancer cette application.")
    exit()

# --- 2. Création de l'application Dash ---
app = Dash(__name__)
server = app.server

# --- 3. Définition de la mise en page (layout) de l'application ---
app.layout = html.Div([
    # Un titre principal pour notre page
    html.H1(
        children='Dashboard des Températures Mondiales en 2023',
        style={'textAlign': 'center'}
    ),

    # Un simple paragraphe de description
    html.Div(
        children='Analyse interactive des températures moyennes journalières de plusieurs capitales mondiales.',
        style={'textAlign': 'center'}
    ),

    # Ce composant 'Graph' est un emplacement vide pour l'instant.
    # Nous y mettrons notre premier graphique à la prochaine étape.
    dcc.Graph(id='placeholder-graph')
])


# --- 4. Lancement de l'application ---
if __name__ == '__main__':
    app.run_server(debug=True)