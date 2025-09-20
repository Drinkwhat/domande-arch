# Configurazione del progetto
PROJECT_NAME = "Analizzatore Compiti Architetture"
VERSION = "1.0.0"

# Percorsi delle cartelle
SCRIPTS_DIR = "scripts"
DATA_DIR = "data"
OUTPUT_DIR = "output"
PDFS_DIR = "pdfs"
DOCS_DIR = "docs"

# File principali
HTML_FILE = "data/data.html"
LINKS_OUTPUT = "output/lista_link.txt"
ANALYSIS_OUTPUT = "output/analisi_domande.txt"
LINKS_VARIABLES = "scripts/links_variable.py"

# Configurazione estrazione domande
PDF_PAGES_TO_EXTRACT = [2, 3]  # pagine 3 e 4 (indice 2 e 3)
MIN_QUESTION_LENGTH = 10

# Configurazione download
DOWNLOAD_DELAY = 1  # secondi tra i download
MAX_RETRIES = 3