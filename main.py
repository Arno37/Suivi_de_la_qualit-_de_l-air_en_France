#!/usr/bin/env python3
"""
Script principal pour la collecte de données de qualité de l'air
Région Centre-Val de Loire

Usage:
    python main.py --source atmo          # Collecte via API Atmo France
    python main.py --source ligair        # Scraping du site Lig'Air
    python main.py --source all           # Toutes les sources
"""

import argparse
import sys
import os
from datetime import datetime

# Ajouter le dossier scripts au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

def run_atmo_collection():
    """Lancer la collecte via l'API Atmo France"""
    try:
        print("🌬️ === COLLECTE ATMO FRANCE ===")
        from scripts.collect.api_atmo import main as atmo_main
        atmo_main()
        print("✅ Collecte Atmo terminée\n")
    except Exception as e:
        print(f"❌ Erreur lors de la collecte Atmo: {e}\n")

def run_ligair_scraping():
    """Lancer le scraping du site Lig'Air"""
    try:
        print("🕷️ === SCRAPING LIG'AIR ===")
        from scripts.collect.scraping_ligair import main as ligair_main
        ligair_main()
        print("✅ Scraping Lig'Air terminé\n")
    except Exception as e:
        print(f"❌ Erreur lors du scraping Lig'Air: {e}\n")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Collecteur de données de qualité de l'air - Centre-Val de Loire",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py --source atmo          # API Atmo France uniquement
  python main.py --source ligair        # Scraping Lig'Air uniquement  
  python main.py --source all           # Toutes les sources
        """
    )
    
    parser.add_argument(
        '--source', 
        choices=['atmo', 'ligair', 'all'],
        default='all',
        help='Source de données à collecter (défaut: all)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='data_output',
        help='Dossier de sortie pour les données (défaut: data_output)'
    )
    
    args = parser.parse_args()
    
    # Créer le dossier de sortie si nécessaire
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"🚀 === COLLECTE DE DONNÉES QUALITÉ DE L'AIR ===")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Dossier de sortie: {args.output_dir}")
    print(f"🎯 Source(s): {args.source}\n")
    
    if args.source in ['atmo', 'all']:
        run_atmo_collection()
    
    if args.source in ['ligair', 'all']:
        run_ligair_scraping()
    
    print("🎉 Collecte terminée !")

if __name__ == "__main__":
    main() 