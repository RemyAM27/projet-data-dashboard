# Fichier: get_data.py
"""
Ce script va :

Définir une liste de capitales mondiales avec leurs coordonnées.

Contacter l'API Open-Meteo (une excellente source de données météo open-source) pour chaque ville.

Demander la température moyenne journalière pour toute l'année 2023.

Compiler toutes les données dans un seul fichier CSV propre.
"""



import requests
import pandas as pd
import os

# --- 1. Définition des villes et de la structure des données ---

# Dictionnaire des capitales mondiales avec leurs coordonnées GPS
# Source: https://gist.github.com/ofou/df09a6834ab87232383c0269399436e2
CITIES = {
    "Paris": {"latitude": 48.8566, "longitude": 2.3522},
    "London": {"latitude": 51.5074, "longitude": -0.1278},
    "New York": {"latitude": 40.7128, "longitude": -74.0060},
    "Tokyo": {"latitude": 35.6895, "longitude": 139.6917},
    "Sydney": {"latitude": -33.8688, "longitude": 151.2093},
    "Cairo": {"latitude": 30.0444, "longitude": 31.2357},
    "Rio de Janeiro": {"latitude": -22.9068, "longitude": -43.1729},
    "Moscow": {"latitude": 55.7558, "longitude": 37.6173},
    "Beijing": {"latitude": 39.9042, "longitude": 116.4074},
    "New Delhi": {"latitude": 28.6139, "longitude": 77.2090},
}

# URL de base de l'API Open-Meteo
API_URL = "https://archive-api.open-meteo.com/v1/archive"

# --- 2. Fonction pour récupérer les données d'une ville ---

def fetch_weather_data(city_name, lat, lon):
    """Récupère les données de température pour une ville donnée pour l'année 2023."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "daily": "temperature_2m_mean", # Température moyenne journalière à 2m du sol
        "timezone": "auto"
    }
    
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        print(f"Données récupérées avec succès pour {city_name}.")
        data = response.json()
        df = pd.DataFrame(data['daily'])
        df['city'] = city_name
        return df
    else:
        print(f"Erreur lors de la récupération des données pour {city_name}. Status: {response.status_code}")
        return None

# --- 3. Script principal pour récupérer et sauvegarder les données ---

if __name__ == "__main__":
    
    all_data = [] # Liste pour stocker les DataFrames de chaque ville
    
    for city, coords in CITIES.items():
        city_df = fetch_weather_data(city, coords['latitude'], coords['longitude'])
        if city_df is not None:
            all_data.append(city_df)
            
    if all_data:
        # Concaténer tous les DataFrames en un seul
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Renommer les colonnes pour plus de clarté
        final_df.rename(columns={"time": "date", "temperature_2m_mean": "temp_mean"}, inplace=True)
        
        # S'assurer que la date est au bon format
        final_df['date'] = pd.to_datetime(final_df['date'])
        
        # Définir le chemin de sauvegarde
        output_dir = os.path.join("data", "raw")
        os.makedirs(output_dir, exist_ok=True) # Créer le dossier s'il n'existe pas
        output_path = os.path.join(output_dir, "temperatures_2023.csv")
        
        # Sauvegarder en fichier CSV
        final_df.to_csv(output_path, index=False)
        
        print(f"\nDonnées compilées et sauvegardées avec succès dans : {output_path}")
        print(f"Aperçu des données :\n{final_df.head()}")