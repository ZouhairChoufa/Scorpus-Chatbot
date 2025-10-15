import os
import requests
import json
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("SCOPUS_API_KEY")
INST_TOKEN = os.getenv("SCOPUS_INST_TOKEN")

def get_all_scopus_results(query, max_results=20):
    """
    Récupère plusieurs pages de résultats de Scopus jusqu'à atteindre max_results.
    """
    headers = {
        "X-ELS-APIKey": API_KEY,
        "X-ELS-Insttoken": INST_TOKEN,
        "Accept": "application/json"
    }
    
    all_entries = []
    start_index = 0
    count_per_page = 25

    print(f"Début de l'extraction pour la requête : '{query}'")

    while start_index < max_results:
        params = {
            "query": query,
            "count": count_per_page,
            "start": start_index,
            "view": "COMPLETE"
        }
        
        url = "https://api.elsevier.com/content/search/scopus"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Erreur {response.status_code} à l'index {start_index}: {response.text}")
            break

        data = response.json()
        entries = data.get('search-results', {}).get('entry', [])
        
        if not entries:
            break
            
        all_entries.extend(entries)
        total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
        print(f"Téléchargé {len(all_entries)} / {min(max_results, total_results)} articles...")

        start_index += count_per_page
        
        if start_index >= total_results:
            break
            
        time.sleep(0.5)

    return {"search-results": {"entry": all_entries}}


if __name__ == "__main__":
    user_theme = input("Veuillez entrer le thème de recherche (en anglais) : ")
    search_query = f'TITLE-ABS-KEY("{user_theme}")'
    
    number_of_articles_to_download = 20
    raw_data = get_all_scopus_results(search_query, max_results=number_of_articles_to_download)

    if raw_data['search-results']['entry']:
        filename = f"{user_theme.replace(' ', '_')}_raw.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        print(f"Les données brutes ont été sauvegardées dans '{filename}'")