# 🌬️ Collecteur de D# 🌬️ Collecteur de Données Qualité de l'Air - Francennées Qualité de l'Air - France

Ce projet collecte et analyse les données de qualité de l'air pour la France depuis différentes sources, répondant aux critères du bloc de compétences 1 (Réaliser la collecte, le stockage et la mise à disposition des données).

## 🎯 Fonctionnalités Principales

1. **Collecte Multi-Source**
   - API Atmo France (données officielles)
   - Web Scraping Lig'Air (données locales)
   - Fichiers CSV (moyennes annuelles)

2. **Stockage Multiple**
   - PostgreSQL : données structurées
   - MongoDB : données historiques (Big Data)
   - Système de fichiers : exports et captures

3. **Technologies Big Data**
   - MongoDB pour le stockage massif
   - Agrégations et analyses
   - Plus de 20M points de données (5 ans × 365 jours × 24h × 5 polluants)

Ce projet collecte et analyse les données de qualité de l'air pour la France à partir de plusieurs sources externes :
- **API Atmo France** : Données officielles nationales
- **Web scraping (Lig'Air)** : Données locales extraites du site Lig'Air
- **Big data** : (prévu, pour de gros volumes)
- **Fichiers plats** : CSV, XLS, etc. (prévu)
- **Bases de données** : (prévu)

## 📁 Structure du Projet

```
PROJET_BLOC_1/
├── scripts/
│   └── collect/
│       ├── api_atmo.py
│       ├── scraping_ligair.py
│       └── ...
├── data_output/
│   ├── api/                  # Données issues de l'API Atmo France
│   ├── scraping_ligair/      # Données issues du scraping Lig'Air
│   ├── files/                # Fichiers CSV, XLS, etc.
│   ├── databases/            # Exports/dumps de bases de données
│   ├── big_data/             # Données massives (prévu)
│   └── processed/            # Données traitées ou filtrées
├── requirements.txt
├── .gitignore
└── README.md
```

- Les **fichiers extraits ou filtrés à partir de l'API* peuvent être placés directement dans `data_output/api/`.
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
# Collecte depuis l'API Atmo France
python scripts/collect/api_atmo.py

# Web scraping Lig'Air
python scripts/collect/scraping_ligair.py

# Collecte et stockage Big Data (MongoDB)
python scripts/collect/big_data_collect.py

# Export vers PostgreSQL
python scripts/collect/bdd_export.py
```

## 📊 Types de Données Collectées

- **API** : Données issues d'appels API (Atmo France)
- **Web scraping** : Données extraites de sites web (Lig'Air)
- **Big data** : Données massives (prévu)
- **Fichiers plats** : CSV, XLS, etc. (prévu)
- **Bases de données** : Exports/dumps SQL, NoSQL (prévu)

## 🛠️ Technologies

- **Python 3.8+**
- **Requests** : Appels API
- **Selenium & BeautifulSoup4** : Web scraping
- **PostgreSQL** : Stockage relationnel
- **MongoDB** : Stockage Big Data
- **SQLAlchemy** : ORM pour PostgreSQL
- **PyMongo** : Client MongoDB
- **python-dotenv** : Gestion des variables d'environnement
- **pandas** : Manipulation des données

## 📝 Notes

- Les sous-dossiers sont prêts à accueillir de nouvelles sources de données.
- Les fichiers extraits/filtrés de l'API peuvent être placés directement dans `api/`.
- Adaptez la structure si vous ajoutez d'autres types de données.

## 📄 Sources de Données

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

**Note** : Ce projet est développé dans le cadre d'un projet de collecte de données environnementales pour la France
