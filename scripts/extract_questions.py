import os
from PyPDF2 import PdfReader
from collections import Counter
import re

def clean_question(question):
    """Rimuove le intestazioni, numeri e altri testi non pertinenti dalla domanda"""
    # Rimuovi le parti che contengono "Architetture degli elaboratori" e simili
    # Dividi per frasi che contengono pattern di intestazione
    parts = re.split(r'Architetture degli elaboratori.*?(?=\d+\)|$)', question, flags=re.IGNORECASE)
    
    # Prendi la prima parte (prima dell'intestazione) se esiste
    if parts and parts[0].strip():
        cleaned = parts[0].strip()
    elif len(parts) > 1 and parts[1].strip():
        # Se la prima parte è vuota, prova con la seconda (dopo l'intestazione)
        cleaned = parts[1].strip()
    else:
        # Come fallback, rimuovi tutto ciò che viene dopo "Architetture degli elaboratori"
        cleaned = re.sub(r'Architetture degli elaboratori.*', '', question, flags=re.IGNORECASE).strip()
    
    # Rimuovi il numero e la parentesi dall'inizio (es: "1) ", "2) ", etc.)
    cleaned = re.sub(r'^\d+\)\s*', '', cleaned).strip()
    
    # Se il risultato è vuoto o troppo corto, scarta la domanda
    if len(cleaned) < 10:
        return None
        
    return cleaned

def extract_questions_from_pages(pdf_path, pages=[2, 3]):  # pagine 3 e 4 (indice 2 e 3)
    """Estrae le domande dalle pagine specificate del PDF"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        for page_num in pages:
            if page_num < len(reader.pages):
                page_text = reader.pages[page_num].extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Cerca domande che iniziano con numero e parentesi, es: "4)"
        # Cattura tutto il testo fino alla prossima domanda numerata o fine riga
        questions = []
        lines = text.split('\n')
        current_question = ""
        
        for line in lines:
            line = line.strip()
            # Se la riga inizia con numero), è una nuova domanda
            if re.match(r'^\d+\)', line):
                if current_question:
                    # Pulisci la domanda dalle intestazioni
                    cleaned_question = clean_question(current_question.strip())
                    if cleaned_question:
                        questions.append(cleaned_question)
                current_question = line
            elif current_question and line:
                # Continua la domanda precedente se non è vuota
                current_question += " " + line
        
        # Aggiungi l'ultima domanda se presente
        if current_question:
            cleaned_question = clean_question(current_question.strip())
            if cleaned_question:
                questions.append(cleaned_question)
            
        return questions
        
    except Exception as e:
        print(f"Errore nel leggere {pdf_path}: {e}")
        return []

def _process_pdfs(pdf_folder):
    """Processa tutti i PDF nella cartella e restituisce i dati"""
    question_counter = Counter()
    file_questions = {}
    total_questions = 0
    
    print("Analizzando i PDF...")
    
    for filename in sorted(os.listdir(pdf_folder)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Elaborando: {filename}")
            
            questions = extract_questions_from_pages(pdf_path)
            file_questions[filename] = questions
            total_questions += len(questions)
            
            for question in questions:
                question_counter[question] += 1
    
    return question_counter, file_questions, total_questions

def _print_statistics(question_counter, file_questions, total_questions):
    """Stampa le statistiche dell'analisi"""
    print("\n" + "="*80)
    print("RISULTATI ANALISI DOMANDE DI TEORIA")
    print("="*80)
    
    print(f"\nTotale PDF analizzati: {len(file_questions)}")
    print(f"Totale domande estratte: {total_questions} (incluse ripetizioni)")
    print(f"Totale domande uniche: {len(question_counter)}")
    print(f"Domande ripetute: {total_questions - len(question_counter)}")
    print(f"Percentuale domande uniche: {(len(question_counter)/total_questions)*100:.1f}%")
    print(f"Media domande per PDF: {total_questions/len(file_questions):.1f}")

def _print_questions_by_frequency(question_counter, file_questions):
    """Stampa le domande ordinate per frequenza"""
    print("\n" + "-"*60)
    print("DOMANDE ORDINATE PER FREQUENZA:")
    print("-"*60)
    
    for question, count in question_counter.most_common():
        print(f"\n[{count}x] {question}")
        
        files_with_question = [filename for filename, questions in file_questions.items() if question in questions]
        
        if len(files_with_question) > 1:
            print(f"    Presente in: {', '.join(files_with_question)}")

def _save_results(question_counter, file_questions, total_questions):
    """Salva i risultati in un file"""
    with open("../output/analisi_domande.txt", "w", encoding="utf-8") as f:
        f.write("ANALISI DOMANDE DI TEORIA - ARCHITETTURE DEGLI ELABORATORI\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Totale PDF analizzati: {len(file_questions)}\n")
        f.write(f"Totale domande estratte: {total_questions} (incluse ripetizioni)\n")
        f.write(f"Totale domande uniche: {len(question_counter)}\n")
        f.write(f"Domande ripetute: {total_questions - len(question_counter)}\n")
        f.write(f"Percentuale domande uniche: {(len(question_counter)/total_questions)*100:.1f}%\n")
        f.write(f"Media domande per PDF: {total_questions/len(file_questions):.1f}\n\n")
        
        # Distribuzione per frequenza
        frequency_distribution = Counter(question_counter.values())
        f.write("DISTRIBUZIONE FREQUENZE:\n")
        for freq in sorted(frequency_distribution.keys(), reverse=True):
            count = frequency_distribution[freq]
            f.write(f"  Frequenza {freq}x: {count} domande\n")
        
        f.write("\nDOMANDE PER FREQUENZA:\n")
        f.write("-"*40 + "\n")
        
        for question, count in question_counter.most_common():
            f.write(f"\n[{count}x] {question}\n")
            
            files_with_question = [filename for filename, questions in file_questions.items() if question in questions]
            
            if len(files_with_question) > 1:
                f.write(f"    File: {', '.join(files_with_question)}\n")

def main():
    """Funzione principale per l'analisi delle domande"""
    pdf_folder = "../pdfs"
    
    if not os.path.exists(pdf_folder):
        print(f"Cartella {pdf_folder} non trovata!")
        return
    
    # Processa i PDF
    question_counter, file_questions, total_questions = _process_pdfs(pdf_folder)
    
    # Stampa statistiche
    _print_statistics(question_counter, file_questions, total_questions)
    
    # Distribuzione frequenze
    frequency_distribution = Counter(question_counter.values())
    print("\nDistribuzione frequenze:")
    for freq in sorted(frequency_distribution.keys(), reverse=True):
        count = frequency_distribution[freq]
        print(f"  Frequenza {freq}x: {count} domande")
    
    # Stampa domande per frequenza
    _print_questions_by_frequency(question_counter, file_questions)
    
    # Domande ripetute
    print("\n" + "-"*60)
    print("SOLO DOMANDE RIPETUTE (frequenza > 1):")
    print("-"*60)
    
    repeated_questions = [(q, c) for q, c in question_counter.items() if c > 1]
    
    if repeated_questions:
        for question, count in sorted(repeated_questions, key=lambda x: x[1], reverse=True):
            print(f"\n[{count}x] {question}")
    else:
        print("Nessuna domanda ripetuta trovata.")
    
    # Salva risultati
    _save_results(question_counter, file_questions, total_questions)
    print("\n\nRisultati salvati in '../output/analisi_domande.txt'")

if __name__ == "__main__":
    main()
