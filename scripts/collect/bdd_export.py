import os
import pandas as pd
from sqlalchemy import create_engine, exc, text
from dotenv import load_dotenv
import unicodedata
import chardet
import logging
import traceback
from urllib.parse import quote_plus

# ==========================================================
# CONFIGURATION ET LOGGING
# ==========================================================
logging.basicConfig(
    filename='import_errors.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ==========================================================
load_dotenv()
REQUIRED_ENV = ['USER', 'PASSWORD', 'HOST', 'DB']
missing_env = [var for var in REQUIRED_ENV if not os.getenv(var)]
if missing_env:
    raise EnvironmentError(f"Variables manquantes : {', '.join(missing_env)}")

# ==========================================================
# CONFIGURATION POSTGRESQL
# ==========================================================
def safe_env(var):
    """Encode une variable d'environnement pour une URL SQLAlchemy"""
    value = os.getenv(var, '')
    if isinstance(value, str):
        value = value.encode('utf-8').decode('utf-8')
    return quote_plus(str(value))

POSTGRES_CONFIG = {
    'user': safe_env("USER"),
    'password': safe_env("PASSWORD"),
    'host': os.getenv("HOST"),
    'port': os.getenv("PORT", "5432"),
    'database': os.getenv("DB"),
    'connect_timeout': 10
}

# ==========================================================
# CONNEXION POSTGRESQL
# ==========================================================
engine = create_engine(
    f'postgresql://{POSTGRES_CONFIG["user"]}:{POSTGRES_CONFIG["password"]}@'
    f'{POSTGRES_CONFIG["host"]}:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["database"]}',
    connect_args={'client_encoding': 'utf8', 'options': '-c client_encoding=utf8'}
)

def test_connection():
    """Test de connexion à la base avec gestion d'erreurs détaillée"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print(f"Connecté à : {result.scalar()}")
        return True
    except exc.OperationalError as e:
        logging.critical(f"Erreur de connexion : {str(e)}")
        print(f"ERREUR CONNEXION : Vérifiez :")
        print(f"- Serveur actif sur {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
        print(f"- Identifiants corrects? USER={POSTGRES_CONFIG['user']}")
        return False

if not test_connection():
    exit(1)

# ==========================================================
# FONCTIONS UTILITAIRES
# ==========================================================
def sanitize_identifier(name):
    """Nettoie les noms de tables/colonnes selon les normes PostgreSQL"""
    name = unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore').decode('ASCII')
    name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
    return name.lower()[:63]

def deep_clean_dataframe(df):
    """Nettoyage approfondi des données"""
    df = df.convert_dtypes()
    for col in df.select_dtypes(include='string'):
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
    return df

def detect_file_encoding(file_path, sample_size=10000):
    """Détection d'encodage avec fallback manuel"""
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    # Test direct avec différents encodages
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(100)
                return encoding
        except UnicodeDecodeError:
            continue
    
    # Si aucun encodage direct ne fonctionne, utiliser chardet
    try:
        with open(file_path, 'rb') as f:
            rawdata = f.read(sample_size)
            result = chardet.detect(rawdata)
            if result['encoding'] and result['confidence'] > 0.8:
                return result['encoding']
    except Exception as e:
        logging.error(f"Erreur détection encodage : {str(e)}")
    
    # Fallback par défaut
    return 'latin1'

def process_csv(file_path):
    """Charge et nettoie un fichier CSV"""
    encoding = detect_file_encoding(file_path)
    print(f"Encodage détecté : {encoding} pour {file_path}")
    try:
        df = pd.read_csv(
            file_path,
            sep=None,
            encoding=encoding,
            engine='python',
            on_bad_lines='warn',
            dtype_backend='pyarrow'
        )
        if df.empty:
            logging.warning(f"Fichier vide : {file_path}")
            return None
        df = deep_clean_dataframe(df)
        df.columns = [sanitize_identifier(col) for col in df.columns]
        return df
    except Exception as e:
        logging.error(f"Échec lecture {file_path} : {str(e)}")
        print(f"ERREUR LECTURE : {file_path}")
        print(f"Message : {str(e)}")
        return None

# ==========================================================
# EXECUTION PRINCIPALE
# ==========================================================
# Obtenir le chemin absolu du dossier du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_folder = os.path.join(project_root, "data_output", "databases", "CSV_to_import")

print(f"Dossier de lecture CSV : {csv_folder}")

# Vérifier si le dossier existe
if not os.path.exists(csv_folder):
    print(f"Erreur : Le dossier {csv_folder} n'existe pas.")
    print("Création du dossier...")
    os.makedirs(csv_folder, exist_ok=True)

# Vérifier s'il y a des fichiers CSV
files = [f for f in os.listdir(csv_folder) if f.lower().endswith('.csv')]
if not files:
    print(f"Attention : Aucun fichier CSV trouvé dans {csv_folder}")
    exit(1)

for filename in os.listdir(csv_folder):
    if not filename.lower().endswith('.csv'):
        continue
    file_path = os.path.join(csv_folder, filename)
    table_name = sanitize_identifier(os.path.splitext(filename)[0])
    print(f"\n{'-'*50}")
    print(f"Traitement de : {filename}")
    print(f"Chemin complet : {file_path}")
    if not os.path.exists(file_path):
        print("FICHIER INTROUVABLE!")
        continue
    df = process_csv(file_path)
    if df is None:
        continue
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            method='multi',
            chunksize=1000
        )
        print(f"SUCCÈS : {len(df)} lignes importées dans {table_name}")
    except Exception as e:
        logging.error(f"Échec import {table_name} : {traceback.format_exc()}")
        print(f"ERREUR IMPORT : {table_name}")
        print(f"Type erreur : {type(e).__name__}")
        print(f"Message : {str(e)}")
        print("Vérifiez :")
        print("- Les types de données PostgreSQL")
        print("- Les noms de colonnes réservés")
        print("- Les contraintes de la table")

print("\nOpération terminée. Vérifiez le fichier 'import_errors.log' pour plus d'informations.")
