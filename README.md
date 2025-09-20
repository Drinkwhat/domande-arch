# 🎓 Analizzatore Compiti Architetture degli Elaboratori

Questo progetto automatizza il processo di raccolta e analisi delle domande d'esame dal corso di **Architetture degli Elaboratori** dell'Università di Bologna.

## 📁 Struttura del Progetto

```
domande-arch/
├── scripts/           # Script Python per automazione
│   ├── extract_links.py       # Estrae link dai file HTML
│   ├── links_variable.py      # Variabili con tutti i link
│   ├── download_compiti.py    # Scarica i PDF dei compiti
│   ├── extract_questions.py   # Estrae domande dai PDF
│   └── main.py               # Script principale
├── data/              # File sorgente
│   └── data.html             # File HTML con i link originali
├── pdfs/              # PDF scaricati dei compiti
├── output/            # Risultati dell'analisi
│   ├── analisi_domande.txt   # Analisi completa delle domande
│   └── lista_link.txt        # Lista di tutti i link estratti
├── docs/              # Documentazione
└── .venv/             # Ambiente virtuale Python
```

## 🚀 Installazione e Setup

### 1. Prerequisiti
- Python 3.8 o superiore
- Ambiente virtuale (già configurato in `.venv/`)

### 2. Attivazione ambiente
```bash
source .venv/bin/activate  # macOS/Linux
# oppure
.venv\Scripts\activate     # Windows
```

### 3. Dipendenze
Le seguenti librerie sono già installate nell'ambiente:
- `beautifulsoup4` - Per parsing HTML
- `requests` - Per download HTTP
- `PyPDF2` - Per lettura PDF

## 🎯 Come Usare il Progetto

### Uso Rapido - Script Principale
```bash
# Dalla directory principale del progetto
python scripts/main.py
```

### Uso Avanzato - Script Individuali

#### 1. Estrazione Link
```bash
python scripts/extract_links.py
```
Estrae tutti i link dal file `data/data.html` e crea:
- `output/lista_link.txt` - Lista completa
- `scripts/links_variable.py` - Variabili Python

#### 2. Download Compiti
```bash
# Scarica tutti i compiti (136 file)
python scripts/download_compiti.py

# Scarica solo un anno specifico
python scripts/download_compiti.py 2024
```

#### 3. Analisi Domande
```bash
python scripts/extract_questions.py
```
Analizza tutti i PDF nella cartella `pdfs/` e genera `output/analisi_domande.txt`

## 📊 Cosa Ottieni

### 1. Lista Completa dei Link
- **136 compiti** dal 2002 al 2025
- URL completi per il download
- Organizzazione per anno

### 2. PDF Scaricati
- File automaticamente scaricati nella cartella `pdfs/`
- Controllo duplicati (non riscarica file esistenti)
- Retry automatico in caso di errori

### 3. Analisi Domande
- **582 domande totali** estratte da 97 PDF
- **211 domande uniche** identificate
- **Frequenza di apparizione** per ogni domanda (da 1x a 6x)
- **File sorgente** per ogni domanda
- Statistiche complete e distribuzione frequenze

## 🔥 Risultati Principali

### Top 5 Domande più Frequenti (6x):
1. Cos'è il "Data Path"?
2. Per quale motivo una memoria cache è in grado di migliorare le prestazioni?
3. Descrivere le principali rappresentazioni dei numeri negativi
4. Descrivere il processo di traduzione da linguaggio alto livello a macchina
5. Descrivere la tassonomia di Flynn nei sistemi paralleli

### Statistiche Generali:
- **97 PDF** analizzati con successo
- **582 domande totali** estratte (incluse ripetizioni)
- **211 domande uniche** identificate
- **36.3% domande uniche** (63.7% ripetute)
- **6.0 domande** per PDF in media

## 🛠 Manutenzione

### Aggiornare i Compiti
1. Aggiorna `data/data.html` con nuovi link
2. Esegui `python scripts/extract_links.py`
3. Scarica nuovi PDF con `python scripts/download_compiti.py`
4. Rigenera l'analisi con `python scripts/extract_questions.py`

### Pulizia
```bash
# Rimuovi file temporanei
rm -rf __pycache__/
rm -rf .DS_Store

# Reset completo PDF (attenzione!)
rm -rf pdfs/
```

## 📈 Utilizzo per lo Studio

### Strategia Consigliata:
1. **Focus sulle domande 4x-6x** - Sono quelle che escono più spesso
2. **Studia per argomento** - Usa la classificazione automatica
3. **Verifica negli anni recenti** - Controlla i pattern temporali
4. **Usa le statistiche** - Per ottimizzare il tempo di studio

### File Principali per lo Studio:
- `output/analisi_domande.txt` - Analisi completa
- Sezione "SOLO DOMANDE RIPETUTE" - Per il ripasso veloce

## 🤝 Contributi

Per migliorare il progetto:
1. Segnala bug o problemi
2. Suggerisci nuove funzionalità
3. Migliora l'accuratezza dell'estrazione domande

## 📝 Note Tecniche

- **Estrazione domande**: Cerca pattern `1)`, `2)`, etc. nelle pagine 3-4 dei PDF
- **Pulizia automatica**: Rimuove intestazioni e numerazione
- **Gestione errori**: Retry automatico e logging dettagliato
- **Encoding**: UTF-8 per tutti i file di testo

## 🎉 Buono Studio!

Questo strumento ti aiuterà a preparare l'esame in modo più efficiente, concentrandoti sulle domande che escono più frequentemente. 📚✨