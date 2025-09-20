#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principale per l'analisi dei compiti di Architetture degli Elaboratori
Coordina tutti gli altri script del progetto
"""

import os
import sys
from pathlib import Path

# Aggiungi il percorso degli script al sys.path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

def print_header():
    """Stampa l'intestazione del programma"""
    print("🎓" + "="*70)
    print("   ANALIZZATORE COMPITI - ARCHITETTURE DEGLI ELABORATORI")
    print("   Università di Bologna - Tool di Automazione")
    print("="*72)

def print_menu():
    """Stampa il menu principale"""
    print("\n📋 MENU PRINCIPALE:")
    print("="*40)
    print("1. 🔗 Estrai link da data.html")
    print("2. 📥 Scarica compiti PDF")
    print("3. 🔍 Analizza domande dai PDF")
    print("4. 🚀 Esegui tutto (pipeline completa)")
    print("5. 📊 Mostra statistiche esistenti")
    print("6. 🧹 Pulisci file temporanei")
    print("0. ❌ Esci")
    print("-"*40)

def check_files():
    """Controlla la presenza dei file necessari"""
    issues = []
    
    # Controlla file sorgente
    if not Path("data/data.html").exists():
        issues.append("❌ File data/data.html non trovato!")
    
    # Controlla script
    required_scripts = [
        "extract_links.py",
        "download_compiti.py", 
        "extract_questions.py"
    ]
    
    for script in required_scripts:
        if not Path(f"scripts/{script}").exists():
            issues.append(f"❌ Script scripts/{script} non trovato!")
    
    return issues

def run_extract_links():
    """Esegue l'estrazione dei link"""
    print("\n🔗 Estrazione link in corso...")
    try:
        # Cambia directory per far funzionare i percorsi relativi
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)  # Torna alla root del progetto
        
        from extract_links import main as extract_main
        extract_main()
        
        os.chdir(original_cwd)
        print("✅ Estrazione link completata!")
        return True
    except Exception as e:
        print(f"❌ Errore nell'estrazione link: {e}")
        return False

def run_download():
    """Menu per il download dei compiti"""
    print("\n📥 OPZIONI DOWNLOAD:")
    print("1. Scarica tutto (136 compiti)")
    print("2. Scarica per anno specifico")
    print("3. Scarica ultimi 3 anni (2023-2025)")
    print("0. Torna al menu")
    
    choice = input("\n👉 Scegli opzione: ").strip()
    
    if choice == "0":
        return True
    
    try:
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        if choice == "1":
            from download_compiti import download_all_compiti
            download_all_compiti()
        elif choice == "2":
            anno = input("📅 Inserisci anno (es. 2024): ").strip()
            from download_compiti import download_by_year
            download_by_year(anno)
        elif choice == "3":
            from download_compiti import download_by_year
            for anno in ["2023", "2024", "2025"]:
                print(f"\n--- Scaricando {anno} ---")
                download_by_year(anno)
        else:
            print("❌ Opzione non valida")
            return False
            
        os.chdir(original_cwd)
        print("✅ Download completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel download: {e}")
        return False

def run_analysis():
    """Esegue l'analisi delle domande"""
    print("\n🔍 Analisi domande in corso...")
    
    # Controlla se ci sono PDF
    pdf_count = len(list(Path("pdfs").glob("*.pdf"))) if Path("pdfs").exists() else 0
    if pdf_count == 0:
        print("⚠️  Nessun PDF trovato nella cartella pdfs/")
        print("   Prima esegui il download dei compiti (opzione 2)")
        return False
    
    print(f"📁 Trovati {pdf_count} PDF da analizzare...")
    
    try:
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        from extract_questions import main as analysis_main
        analysis_main()
        
        os.chdir(original_cwd)
        print("✅ Analisi completata!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nell'analisi: {e}")
        return False

def run_full_pipeline():
    """Esegue la pipeline completa"""
    print("\n🚀 PIPELINE COMPLETA")
    print("Questo processo può richiedere molto tempo...")
    
    confirm = input("Vuoi continuare? (s/n): ").lower().strip()
    if confirm not in ['s', 'si', 'sì', 'y', 'yes']:
        print("❌ Pipeline annullata")
        return
    
    steps = [
        ("🔗 Estrazione link", run_extract_links),
        ("📥 Download compiti", lambda: run_download_all()),
        ("🔍 Analisi domande", run_analysis)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Pipeline fermata al passo: {step_name}")
            return
    
    print("\n🎉 Pipeline completata con successo!")

def run_download_all():
    """Scarica tutti i compiti per la pipeline"""
    try:
        original_cwd = os.getcwd()
        os.chdir(Path(__file__).parent.parent)
        
        from download_compiti import download_all_compiti
        download_all_compiti()
        
        os.chdir(original_cwd)
        return True
    except Exception as e:
        print(f"❌ Errore nel download: {e}")
        return False

def show_statistics():
    """Mostra le statistiche esistenti"""
    print("\n📊 STATISTICHE ESISTENTI:")
    
    # Controlla file di output
    output_files = {
        "Lista link": "output/lista_link.txt",
        "Analisi domande": "output/analisi_domande.txt"
    }
    
    for name, file_path in output_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {name}: {file_path} ({size} bytes)")
        else:
            print(f"❌ {name}: Non ancora generato")
    
    # Conta PDF
    pdf_count = len(list(Path("pdfs").glob("*.pdf"))) if Path("pdfs").exists() else 0
    print(f"📁 PDF scaricati: {pdf_count}")
    
    # Mostra sommario se disponibile
    if Path("output/analisi_domande.txt").exists():
        print(f"\n📋 Sommario analisi (prime righe):")
        print("-" * 40)
        with open("output/analisi_domande.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            for line in lines:
                print(line.rstrip())
        if len(lines) >= 10:
            print("... (file completo in output/analisi_domande.txt)")

def clean_temp_files():
    """Rimuove file temporanei"""
    print("\n🧹 Pulizia file temporanei...")
    
    temp_patterns = [
        "__pycache__",
        ".DS_Store",
        "*.pyc",
        ".pytest_cache"
    ]
    
    cleaned = 0
    for pattern in temp_patterns:
        for file_path in Path(".").rglob(pattern):
            if file_path.exists():
                if file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                cleaned += 1
                print(f"🗑️  Rimosso: {file_path}")
    
    if cleaned == 0:
        print("✨ Nessun file temporaneo da rimuovere")
    else:
        print(f"✅ Rimossi {cleaned} file/cartelle temporanee")

def main():
    """Funzione principale"""
    print_header()
    
    # Controlla i file necessari
    issues = check_files()
    if issues:
        print("\n⚠️  PROBLEMI RILEVATI:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 Suggerimento: Controlla la struttura del progetto")
        return
    
    while True:
        print_menu()
        choice = input("👉 Scegli un'opzione (0-6): ").strip()
        
        try:
            if choice == "0":
                print("\n👋 Arrivederci!")
                break
            elif choice == "1":
                run_extract_links()
            elif choice == "2":
                run_download()
            elif choice == "3":
                run_analysis()
            elif choice == "4":
                run_full_pipeline()
            elif choice == "5":
                show_statistics()
            elif choice == "6":
                clean_temp_files()
            else:
                print("❌ Opzione non valida. Scegli un numero da 0 a 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrotto dall'utente. Arrivederci!")
            break
        except Exception as e:
            print(f"❌ Errore inaspettato: {e}")
        
        input("\n📝 Premi INVIO per continuare...")

if __name__ == "__main__":
    main()