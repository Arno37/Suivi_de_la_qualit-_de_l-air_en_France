# 🌬️ Collecteur de Données Qualité de l'Air - France

Ce projet collecte et analyse les données de qualité de l'air pour la France, répondant aux critères du bloc de compétences 1 (Réaliser la collecte, le stockage et la mise à disposition des données).

## 🎯 Réalisations

1. **Collecte Multi-Source**
   - API Atmo France : Données officielles nationales
   - Web Scraping Lig'Air : Données locales en temps réel
   - Fichiers CSV : Export des moyennes annuelles

2. **Stockage Multiple**
   - PostgreSQL : 1,081 mesures structurées
     * CO : 19 mesures
     * NO₂ : 392 mesures
     * PM₁₀ : 361 mesures
     * PM₂.₅ : 260 mesures
     * C₆H₆ : 49 mesures
   - MongoDB : Données historiques (Big Data)
   - Système de fichiers : Exports et captures d'écran

3. **Technologies Big Data**
   - MongoDB : Stockage de données massives
   - Volume : >20M points de données
     * 5 ans de données (2020-2024)
     * 365 jours par an
     * 24 mesures par jour
     * 5 polluants différents
   - Agrégations et analyses temporelles

## 📁 Structure du Projet

```bash
PROJET_BLOC_1/
├── scripts/
│   └── collect/
│       ├── api_atmo.py         # Collecte API Atmo France
│       ├── scraping_ligair.py  # Web Scraping
│       ├── bdd_export.py       # Export PostgreSQL
│       └── big_data_collect.py # Collecte Big Data
├── data_output/
│   ├── api/                  # Données API
│   ├── scraping/            # Captures d'écran et données
│   ├── databases/           # Exports CSV et SQL
│   └── big_data/           # Données MongoDB
└── requirements.txt
```

## 🚀 Installation

1. **Prérequis**
   - Python 3.8+
   - PostgreSQL 13+
   - MongoDB
   - Chrome (pour Selenium)

2. **Dépendances Python**
```bash
pip install -r requirements.txt
```

3. **Configuration**
```env
# .env
ATMO_USERNAME=votre_username
ATMO_PASSWORD=votre_password
ANNEE=2024

# PostgreSQL
USER=postgres
PASSWORD=votre_password
DB=postgres
HOST=localhost
PORT=5432
```

## 📊 Types de Données

1. **API Atmo France**
   - Émissions régionales
   - Concentrations horaires
   - Indices qualité air

2. **Web Scraping (Lig'Air)**
   - Données temps réel
   - Validation visuelle
   - Format : JSON + PNG

3. **PostgreSQL**
   - Moyennes annuelles par polluant
   - 5 polluants principaux
   - 1,081 mesures totales

4. **MongoDB (Big Data)**
   - Données historiques 2020-2024
   - Multiple types de mesures
   - Agrégations temporelles
   - >20M points de données

## 🛠️ Technologies

- **Collecte** :
  * Requests : API
  * Selenium : Web Scraping
  * pandas : Manipulation données

- **Stockage** :
  * PostgreSQL : Données structurées
  * MongoDB : Big Data
  * SQLAlchemy : ORM
  * PyMongo : Client MongoDB

## 📈 Utilisation

```bash
# Collecte API
python scripts/collect/api_atmo.py

# Web Scraping
python scripts/collect/scraping_ligair.py

# Export PostgreSQL
python scripts/collect/bdd_export.py

# Collecte Big Data
python scripts/collect/big_data_collect.py
```

## 📝 Notes

- Les données sont organisées par source
- MongoDB gère les données historiques volumineuses
- PostgreSQL stocke les moyennes annuelles
- Validation visuelle du scraping par captures d'écran

---

Projet développé dans le cadre du bloc de compétences 1 : Réaliser la collecte, le stockage et la mise à disposition des données d'un projet en intelligence artificielle.
