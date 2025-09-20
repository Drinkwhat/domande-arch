#!/usr/bin/env python3
"""
Script per scaricare tutti i compiti (PDF e DOC) nella cartella pdfs
"""

import os
import requests
from pathlib import Path
import time
from urllib.parse import urlparse
from links_variable import COMPITI_DICT, TOTALE_COMPITI

def create_download_folder(folder_path="pdfs"):
    """Crea la cartella di download se non esiste"""
    Path(folder_path).mkdir(exist_ok=True)
    return folder_path

def get_filename_from_url(url):
    """Estrae il nome del file dall'URL"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename

def download_file(url, filename, folder_path, max_retries=3):
    """Scarica un singolo file con retry automatico"""
    file_path = os.path.join(folder_path, filename)
    
    # Controlla se il file esiste già
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        if file_size > 0:  # File non vuoto
            print(f"✓ Già presente: {filename} ({file_size} bytes)")
            return True
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Scarica il file con retry
    for attempt in range(max_retries):
        try:
            print(f"📥 Scaricando: {filename} (tentativo {attempt + 1}/{max_retries})")
            
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Salva il file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(file_path)
            print(f"✅ Completato: {filename} ({file_size} bytes)")
            return True
            
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"❌ Errore nel tentativo {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("⏳ Pausa di 2 secondi...")
                time.sleep(2)
            else:
                print(f"💥 Fallito dopo {max_retries} tentativi: {filename}")
                return False

def _print_download_stats(success_count, failed_files):
    """Stampa le statistiche finali del download"""
    print("\n" + "=" * 60)
    print("📊 STATISTICHE FINALI")
    print("=" * 60)
    print(f"✅ Scaricati con successo: {success_count}")
    print(f"❌ Falliti: {len(failed_files)}")
    print(f"📈 Percentuale successo: {(success_count/TOTALE_COMPITI)*100:.1f}%")
    
    if failed_files:
        print("\n❌ File falliti:")
        for failed in failed_files:
            print(f"   - {failed['nome']} ({failed['filename']})")

def _print_folder_stats(folder_path):
    """Stampa le statistiche della cartella"""
    downloaded_files = list(Path(folder_path).glob("*"))
    print(f"\n📁 File nella cartella '{folder_path}': {len(downloaded_files)}")
    
    extensions = {}
    total_size = 0
    for file_path in downloaded_files:
        if file_path.is_file():
            ext = file_path.suffix.lower()
            size = file_path.stat().st_size
            total_size += size
            
            if ext not in extensions:
                extensions[ext] = {'count': 0, 'size': 0}
            extensions[ext]['count'] += 1
            extensions[ext]['size'] += size
    
    print("\n📈 Per tipo di file:")
    for ext, data in extensions.items():
        size_mb = data['size'] / (1024 * 1024)
        print(f"   {ext}: {data['count']} file ({size_mb:.1f} MB)")
    
    total_size_mb = total_size / (1024 * 1024)
    print(f"\n💾 Spazio totale occupato: {total_size_mb:.1f} MB")

def download_all_compiti(folder_path="../pdfs", delay=1):
    """Scarica tutti i compiti"""
    print(f"🚀 Inizio download di {TOTALE_COMPITI} compiti...")
    print(f"📁 Cartella di destinazione: {os.path.abspath(folder_path)}")
    print("=" * 60)
    
    create_download_folder(folder_path)
    
    success_count = 0
    failed_files = []
    
    for i, compito in enumerate(COMPITI_DICT, 1):
        url = compito['url_completo']
        filename = get_filename_from_url(url)
        
        print(f"\n[{i}/{TOTALE_COMPITI}] {compito['nome']}")
        
        if download_file(url, filename, folder_path):
            success_count += 1
        else:
            failed_files.append({
                'nome': compito['nome'],
                'url': url,
                'filename': filename
            })
        
        if i < TOTALE_COMPITI:
            time.sleep(delay)
    
    _print_download_stats(success_count, failed_files)
    _print_folder_stats(folder_path)

def download_by_year(year, folder_path="../pdfs"):
    """Scarica solo i compiti di un anno specifico"""
    from links_variable import get_compiti_by_year, get_url_by_nome
    
    compiti_anno = get_compiti_by_year(year)
    if not compiti_anno:
        print(f"❌ Nessun compito trovato per l'anno {year}")
        return
    
    print(f"📅 Scaricando {len(compiti_anno)} compiti dell'anno {year}...")
    create_download_folder(folder_path)
    
    success_count = 0
    for i, nome_compito in enumerate(compiti_anno, 1):
        url = get_url_by_nome(nome_compito)
        filename = get_filename_from_url(url)
        
        print(f"[{i}/{len(compiti_anno)}] {nome_compito}")
        
        if download_file(url, filename, folder_path):
            success_count += 1
        
        time.sleep(1)  # Pausa tra i download
    
    print(f"\n✅ Completati: {success_count}/{len(compiti_anno)} file dell'anno {year}")

def main():
    """Funzione principale"""
    import sys
    
    if len(sys.argv) > 1:
        # Scarica solo un anno specifico
        year = sys.argv[1]
        download_by_year(year)
    else:
        # Scarica tutto
        print("⚠️  ATTENZIONE: Stai per scaricare 136 file!")
        print("   Questo potrebbe richiedere diversi minuti.")
        print("   Per scaricare solo un anno, usa: python download_compiti.py 2024")
        
        response = input("\n🤔 Vuoi continuare? (s/n): ").lower().strip()
        if response in ['s', 'si', 'sì', 'y', 'yes']:
            download_all_compiti()
        else:
            print("❌ Download annullato.")

if __name__ == "__main__":
    main()