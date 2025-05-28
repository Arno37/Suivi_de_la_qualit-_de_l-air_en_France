import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def main():
    """Fonction principale pour la collecte Atmo France"""
    load_dotenv()
    USERNAME = os.getenv("ATMO_USERNAME")
    PASSWORD = os.getenv("ATMO_PASSWORD")
    ANNEE = os.getenv("ANNEE", "2024")  # Valeur par défaut
    
    print(f"🔐 Authentification Atmo France...")
    
    # Authentification
    LOGIN_URL = "https://admindata.atmo-france.org/api/login"
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        login_response = requests.post(LOGIN_URL, json=login_payload)
        login_response.raise_for_status()
        token = login_response.json()["token"]
        print("✅ Authentification réussie")
    except Exception as e:
        print(f"❌ Erreur d'authentification: {e}")
        return
    
    # Toujours enregistrer dans data_output/api/ à la racine du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "data_output", "api")
    os.makedirs(output_dir, exist_ok=True)
    
    # Construction du filtre dans l'URL
    layer_id = 119
    search_filter = json.dumps({"annee": {"operator": "=", "value": ANNEE}})
    from urllib.parse import quote
    search_filter_encoded = quote(search_filter)
    
    print(f"📊 Collecte des émissions régionales {ANNEE}...")
    
    url = f"https://admindata.atmo-france.org/api/data/{layer_id}/{search_filter_encoded}"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print("Statut de la réponse :", response.status_code)
        response.raise_for_status()
        data = response.json()
        
        # Sauvegarde avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"emissions_regions_{ANNEE}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Fichier {filename} sauvegardé avec succès.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la collecte des émissions: {e}")
    
    print(f"📈 Collecte des épisodes historiques {ANNEE}...")
    
    # Nouvelle URL pour les épisodes historiques (GeoJSON)
    url = f"https://admindata.atmo-france.org/api/v2/data/episodes/historique?format=geojson&date={ANNEE}-12-31&date_historique={ANNEE}-01-01"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Sauvegarde du fichier JSON avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"episodes_historique_{ANNEE}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(f"✅ Fichier {filename} sauvegardé avec succès.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la collecte des épisodes: {e}")

if __name__ == "__main__":
    main() 