import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote

def connect_mongodb():
    """Connexion à MongoDB"""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['atmo_big_data']
        print("✅ Connexion MongoDB réussie")
        return db
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB: {e}")
        return None

def get_atmo_token():
    """Obtenir un token d'authentification Atmo France"""
    load_dotenv()
    USERNAME = os.getenv("ATMO_USERNAME")
    PASSWORD = os.getenv("ATMO_PASSWORD")
    
    LOGIN_URL = "https://admindata.atmo-france.org/api/login"
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        login_response = requests.post(LOGIN_URL, json=login_payload)
        login_response.raise_for_status()
        token = login_response.json()["token"]
        print("✅ Authentification Atmo France réussie")
        return token
    except Exception as e:
        print(f"❌ Erreur d'authentification: {e}")
        return None

def collect_historical_data(token, start_year=2020, end_year=2024):
    """Collecter les données historiques d'Atmo France"""
    if not token:
        return []
    
    all_data = []
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }
    
    # Différents types de données à collecter
    layer_configs = [
        {"id": 119, "name": "emissions_regionales"},
        {"id": 120, "name": "concentrations_horaires"},
        {"id": 121, "name": "indices_qualite_air"}
    ]
    
    for year in range(start_year, end_year + 1):
        print(f"📊 Collecte des données pour {year}...")
        for layer in layer_configs:
            try:
                search_filter = json.dumps({"annee": {"operator": "=", "value": str(year)}})
                search_filter_encoded = quote(search_filter)
                url = f"https://admindata.atmo-france.org/api/data/{layer['id']}/{search_filter_encoded}"
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Ajouter des métadonnées
                for item in data:
                    item['year'] = year
                    item['data_type'] = layer['name']
                    item['collected_at'] = datetime.now().isoformat()
                
                all_data.extend(data)
                print(f"✅ {len(data)} enregistrements collectés pour {layer['name']} {year}")
                
            except Exception as e:
                print(f"❌ Erreur lors de la collecte {layer['name']} {year}: {e}")
    
    return all_data

def save_to_mongodb(db, data):
    """Sauvegarder les données dans MongoDB"""
    if not db or not data:
        return
    
    try:
        # Création des collections
        pollution_data = db.pollution_data
        
        # Insertion des données
        result = pollution_data.insert_many(data)
        print(f"✅ {len(result.inserted_ids)} documents insérés dans MongoDB")
        
        # Création des index pour optimiser les requêtes
        pollution_data.create_index([("year", 1)])
        pollution_data.create_index([("data_type", 1)])
        pollution_data.create_index([("collected_at", 1)])
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde MongoDB: {e}")

def perform_aggregations(db):
    """Effectuer des agrégations sur les données"""
    if not db:
        return
    
    try:
        pollution_data = db.pollution_data
        
        # Exemple d'agrégation 1: Nombre de mesures par année et type
        pipeline1 = [
            {"$group": {
                "_id": {
                    "year": "$year",
                    "data_type": "$data_type"
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.year": 1}}
        ]
        
        results = list(pollution_data.aggregate(pipeline1))
        print("\n📊 Statistiques de collecte:")
        for result in results:
            print(f"Année {result['_id']['year']} - {result['_id']['data_type']}: {result['count']} mesures")
        
    except Exception as e:
        print(f"❌ Erreur lors des agrégations: {e}")

def main():
    """Fonction principale"""
    print("🚀 Démarrage de la collecte Big Data...")
    
    # Connexion à MongoDB
    db = connect_mongodb()
    if not db:
        return
    
    # Authentification Atmo France
    token = get_atmo_token()
    if not token:
        return
    
    # Collecte des données historiques
    data = collect_historical_data(token)
    
    # Sauvegarde dans MongoDB
    save_to_mongodb(db, data)
    
    # Agrégations
    perform_aggregations(db)
    
    print("✨ Opération terminée")

if __name__ == "__main__":
    main()
