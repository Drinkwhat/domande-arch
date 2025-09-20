# 🚀 Quick Start Guide

## Avvio Rapido
```bash
# 1. Attiva ambiente virtuale
source .venv/bin/activate

# 2. Lancia script principale
python scripts/main.py
```

## Opzioni Veloci
```bash
# Estrai link
python scripts/extract_links.py

# Scarica anno specifico
python scripts/download_compiti.py 2024

# Analizza domande
python scripts/extract_questions.py
```

## Struttura Progetto
```
📁 domande-arch/
├── scripts/     # Script Python
├── data/        # File sorgente  
├── pdfs/        # PDF scaricati
├── output/      # Risultati analisi
└── docs/        # Documentazione
```

## File Principali
- `README.md` - Documentazione completa
- `scripts/main.py` - Script principale interattivo
- `output/analisi_domande.txt` - Risultati analisi domande