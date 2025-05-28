# 🌬️ Collecteur de Données Qualité de l'Air - Centre-Val de Loire

Ce projet collecte et analyse les données de qualité de l'air pour la région Centre-Val de Loire à partir de plusieurs sources externes :
- **API Atmo France** : Données officielles nationales
- **Web scraping (Lig'Air)** : Données locales extraites du site Lig'Air
- **Big data** : (prévu, pour de gros volumes)
- **Fichiers plats** : CSV, XLS, etc. (prévu)
- **Bases de données** : (prévu)

## 📁 Structure du Projet

```
PROJET_BLOC_1/
├── main.py
├── scripts/
├── utils/
├── data_output/
│   ├── api/                  # Données issues de l'API Atmo France
│   │   ├── atmo_emissions_2024.json
│   │   ├── atmo_emissions_all_regions.json
│   │   ├── atmo_episodes_2024.csv
│   │   ├── episodes_historique_2024_20250528_1226.csv
│   │   └── centre_val_loire_emissions.json   # (extraction/filtrage API)
│   ├── scraping_ligair/      # Données issues du scraping Lig'Air
│   │   ├── scraping_ligair_data.json
│   │   └── scraping_ligair_screenshot.png
│   ├── big_data/            # (prévu pour de gros volumes)
│   ├── files/               # (prévu pour fichiers CSV, XLS, etc.)
│   └── databases/           # (prévu pour exports/dumps de bases de données)
├── requirements.txt
├── .gitignore
└── README.md
```

- Les **fichiers extraits ou filtrés à partir de l'API** (ex : `centre_val_loire_emissions.json`) peuvent être placés directement dans `data_output/api/`.
- Les sous-dossiers vides sont prêts à accueillir de nouvelles sources si besoin.

## 🚀 Installation

1. **Cloner le projet :**
```bash
git clone <url-du-repo>
cd PROJET_BLOC_1
```

2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Configuration (pour l'API Atmo) :**
Créer un fichier `.env` avec vos identifiants :
```env
ATMO_USERNAME=votre_username
ATMO_PASSWORD=votre_password
ANNEE=2024
```

## 🎯 Utilisation

### Script Principal (Recommandé)

```bash
python main.py --source all
```

### Scripts Individuels

```bash
python scripts/collect_atmo.py
python scripts/scraping_ligair_selenium.py
```

## 📊 Types de Données Collectées

- **API** : Données issues d'appels API (Atmo France)
- **Web scraping** : Données extraites de sites web (Lig'Air)
- **Big data** : Données massives (prévu)
- **Fichiers plats** : CSV, XLS, etc. (prévu)
- **Bases de données** : Exports/dumps SQL, NoSQL (prévu)

## 🛠️ Technologies

- **Python 3.8+**
- **Requests**
- **Selenium**
- **BeautifulSoup4**
- **python-dotenv**
- **webdriver-manager**

## 📝 Notes

- Les sous-dossiers sont prêts à accueillir de nouvelles sources de données.
- Les fichiers extraits/filtrés de l'API peuvent être placés directement dans `api/`.
- Adaptez la structure si vous ajoutez d'autres types de données.

## �� Sources de Données

### 1. API Atmo France
- **URL** : https://admindata.atmo-france.org/
- **Données** : Émissions régionales, épisodes de pollution historiques
- **Format** : JSON, CSV
- **Authentification** : Requise

### 2. Lig'Air (Scraping)
- **URL** : https://www.ligair.fr/
- **Données** : Indices ATMO et Pollen pour 6 villes
- **Villes** : Bourges, Chartres, Châteauroux, Tours, Blois, Orléans
- **Format** : JSON
- **Méthode** : Selenium WebDriver

## 📈 Données Collectées

### API Atmo France
- `emissions_regions_YYYY_timestamp.json` : Émissions par région
- `episodes_historique_YYYY_timestamp.csv` : Historique des épisodes

### Lig'Air
- `ligair_selenium_improved_timestamp.json` : Indices des villes
- `ligair_screenshot_timestamp.png` : Screenshots de debug

## 🔧 Configuration Avancée

### Variables d'Environnement (.env)
```env
# Authentification Atmo France
ATMO_USERNAME=votre_username
ATMO_PASSWORD=votre_password

# Année de collecte
ANNEE=2024

# Configuration Selenium (optionnel)
SELENIUM_HEADLESS=false
SELENIUM_TIMEOUT=60
```

### Selenium
Le script utilise ChromeDriver qui est installé automatiquement via `webdriver-manager`. Assurez-vous d'avoir Chrome installé sur votre système.

## 🐛 Debug et Dépannage

### Problèmes courants

1. **Erreur d'authentification Atmo** :
   - Vérifiez vos identifiants dans le fichier `.env`
   - Contactez Atmo France pour obtenir un accès

2. **Selenium ne trouve pas Chrome** :
   - Installez Google Chrome
   - Vérifiez que Chrome est dans le PATH

3. **Timeout lors du scraping Lig'Air** :
   - Le site charge les données dynamiquement
   - Augmentez le timeout dans le script
   - Vérifiez votre connexion internet

### Script de Debug
```bash
python utils/debug_scraping.py
```

## 📝 Logs

Les logs sont automatiquement générés dans le dossier `logs/` avec horodatage.

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Note** : Ce projet est développé dans le cadre d'un projet de collecte de données environnementales pour la France.
