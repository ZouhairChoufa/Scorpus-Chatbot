import pandas as pd
import json
import glob

def create_relational_database_from_all_themes():
    """
    Trouve tous les fichiers *_raw.json, les combine, et les structure.
    """
    json_files = glob.glob('*_raw.json')
    if not json_files:
        print("Aucun fichier de données brut (*_raw.json) trouvé. Veuillez d'abord exécuter 'extract_data.py'.")
        return

    print(f"Fichiers trouvés à combiner : {json_files}")

    all_entries = []
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get('search-results', {}).get('entry', [])
            all_entries.extend(entries)
            
    articles_list = []
    authors_list = []
    links_list = []
    
    for item in all_entries:
        scopus_id = item.get('dc:identifier', '').replace('SCOPUS_ID:', '')
        if not scopus_id or not item.get('dc:description'):
            continue

        articles_list.append({
            'article_id': scopus_id,
            'doi': item.get('prism:doi'),
            'title': item.get('dc:title'),
            'publication_name': item.get('prism:publicationName'),
            'year': item.get('prism:coverDate', '').split('-')[0],
            'abstract': item.get('dc:description'),
            'keywords': item.get('authkeywords', '').replace(' | ', ', ')
        })

        if 'author' in item:
            for author in item['author']:
                author_id = author.get('authid') 
                if author_id:
                    authors_list.append({
                        'author_id': author_id,
                        'author_name': author.get('authname')
                    })
                    links_list.append({'article_id': scopus_id, 'author_id': author_id})

    articles_df = pd.DataFrame(articles_list).drop_duplicates(subset='article_id').reset_index(drop=True)
    authors_df = pd.DataFrame(authors_list).drop_duplicates(subset='author_id').reset_index(drop=True)
    links_df = pd.DataFrame(links_list).drop_duplicates()

    articles_df.to_csv('articles.csv', index=False)
    authors_df.to_csv('authors.csv', index=False)
    links_df.to_csv('article_author_links.csv', index=False)
    
    print("Base de données relationnelle combinée créée avec succès :")
    print(f"- {len(articles_df)} articles uniques dans articles.csv")
    print(f"- {len(authors_df)} auteurs uniques dans authors.csv")

if __name__ == "__main__":
    create_relational_database_from_all_themes()