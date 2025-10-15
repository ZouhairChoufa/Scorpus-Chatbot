import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

def create_semantic_index(data_file='articles.csv'):
    """
    Crée un index sémantique FAISS à partir des résumés d'articles.
    """
    df = pd.read_csv(data_file) 
    df['abstract'] = df['abstract'].astype(str)
    
    print("Chargement du modèle Sentence Transformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Vectorisation des résumés... (cela peut prendre un moment)")
    abstract_vectors = model.encode(df['abstract'].tolist(), show_progress_bar=True) 

    print("Création de l'index FAISS...")
    index = faiss.IndexFlatL2(abstract_vectors.shape[1]) 
    index.add(np.array(abstract_vectors, dtype=np.float32))

    faiss.write_index(index, 'articles.index')
    
    df.to_pickle('articles_df.pkl')
    print("L'index FAISS ('articles.index') et le dataframe ('articles_df.pkl') ont été créés.")

if __name__ == "__main__":
    create_semantic_index()