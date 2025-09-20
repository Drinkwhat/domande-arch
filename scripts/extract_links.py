#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per estrarre tutti i link dal file data.html e generare variabili Python
"""

from bs4 import BeautifulSoup
import re

def extract_links_from_html(html_file):
    """Estrae tutti i link dal file HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        
        # Salta il link "To Parent Directory"
        if href != '/arc/' and not href.startswith('['):
            links.append({
                'url': href,
                'text': text,
                'full_url': f"https://biolab.csr.unibo.it{href}"
            })
    
    return links

def generate_statistics(links):
    """Genera statistiche sui link per anno"""
    years = {}
    for link in links:
        match = re.search(r'(\d{4})_', link['text'])
        if match:
            year = match.group(1)
            years[year] = years.get(year, 0) + 1
    return years

def save_links_to_file(links, output_file):
    """Salva i link in un file di testo con statistiche"""
    years = generate_statistics(links)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Lista di tutti i link estratti da data.html\n")
        f.write("=" * 50 + "\n\n")
        
        # Lista semplice
        f.write("LISTA SEMPLICE:\n")
        f.write("-" * 20 + "\n")
        for i, link in enumerate(links, 1):
            f.write(f"{i}. {link['text']}\n")
        
        # URL completi
        f.write("\n\nURL COMPLETI:\n")
        f.write("-" * 20 + "\n")
        for i, link in enumerate(links, 1):
            f.write(f"{i}. {link['full_url']}\n")
        
        # Statistiche
        f.write("\n\nSTATISTICHE:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Totale link trovati: {len(links)}\n")
        f.write(f"Anni rappresentati: {len(years)}\n\n")
        
        f.write("Link per anno:\n")
        for year in sorted(years.keys()):
            f.write(f"  {year}: {years[year]} compiti\n")

def generate_links_variable(links, output_file):
    """Genera un file Python con i link come variabili"""
    # Raggruppa per anno
    YEAR_PATTERN = r'(\d{4})_'
    years = {}
    for link in links:
        match = re.search(YEAR_PATTERN, link['text'])
        if match:
            year = match.group(1)
            if year not in years:
                years[year] = []
            years[year].append(link)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Link dei compiti come variabili Python - Generato automaticamente\n')
        f.write('"""\n\n')
        
        # Lista nomi
        f.write('COMPITI_NOMI = [\n')
        for link in links:
            f.write(f'    "{link["text"]}",\n')
        f.write(']\n\n')
        
        # Lista URL completi
        f.write('COMPITI_URL = [\n')
        for link in links:
            f.write(f'    "{link["full_url"]}",\n')
        f.write(']\n\n')
        
        # Dizionario completo
        f.write('COMPITI_DICT = [\n')
        for link in links:
            f.write(f'    {{"nome": "{link["text"]}", ')
            f.write(f'"url_relativo": "{link["url"]}", ')
            f.write(f'"url_completo": "{link["full_url"]}"}},\n')
        f.write(']\n\n')
        
        # Statistiche
        f.write(f'TOTALE_COMPITI = {len(links)}\n\n')
        
        # Per anno
        f.write('COMPITI_PER_ANNO = {\n')
        for year in sorted(years.keys()):
            f.write(f'    "{year}": [\n')
            for link in years[year]:
                f.write(f'        "{link["text"]}",\n')
            f.write('    ],\n')
        f.write('}\n\n')
        
        # Funzioni di utilità
        f.write('def get_compiti_by_year(anno):\n')
        f.write('    """Restituisce i compiti per un anno specifico"""\n')
        f.write('    return COMPITI_PER_ANNO.get(str(anno), [])\n\n')
        
        f.write('def get_url_by_nome(nome_compito):\n')
        f.write('    """Restituisce l\'URL completo dato il nome del compito"""\n')
        f.write('    for compito in COMPITI_DICT:\n')
        f.write('        if compito["nome"] == nome_compito:\n')
        f.write('            return compito["url_completo"]\n')
        f.write('    return None\n\n')
        
        f.write('def get_anni_disponibili():\n')
        f.write('    """Restituisce la lista degli anni disponibili"""\n')
        f.write('    return sorted(COMPITI_PER_ANNO.keys())\n')

def main():
    """Funzione principale"""
    html_file = '../data/data.html'
    output_file = '../output/lista_link.txt'
    var_file = 'links_variable.py'
    
    print("Estrazione link da data.html...")
    
    try:
        links = extract_links_from_html(html_file)
        
        if links:
            print(f"Trovati {len(links)} link")
            
            # Salva in file di testo
            save_links_to_file(links, output_file)
            print(f"Link salvati in: {output_file}")
            
            # Genera file con variabili Python
            generate_links_variable(links, var_file)
            print(f"Variabili generate in: {var_file}")
            
            # Mostra statistiche
            stats = generate_statistics(links)
            print("\nStatistiche:")
            print(f"- Totale compiti: {stats['totale']}")
            print(f"- Anni disponibili: {sorted(stats['anni'].keys())}")
            
            print("\nTop anni per numero di compiti:")
            for year, count in stats['top_anni']:
                print(f"  {year}: {count} compiti")
        else:
            print("Nessun link trovato")
            
    except FileNotFoundError:
        print(f"File {html_file} non trovato")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()