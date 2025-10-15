import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Scopus Chatbot", layout="wide")

st.markdown("""
<style>
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }
    .user-message {
        background-color: #2b313e;
        color: #fafafa;
        border-radius: 1rem;
        padding: 0.75rem;
        margin-bottom: 1rem;
        max-width: 60%;
        word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def load_faiss_index():
    try:
        return faiss.read_index('articles.index')
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'index. Avez-vous exécuté 'create_index.py' ? Détails: {e}")
        return None

@st.cache_data
def load_data():
    try:
        articles_df = pd.read_csv('articles.csv')
        authors_df = pd.read_csv('authors.csv')
        links_df = pd.read_csv('article_author_links.csv')
        return articles_df, authors_df, links_df
    except FileNotFoundError as e:
        st.error(f"Erreur: Le fichier {e.filename} est manquant. Veuillez exécuter les scripts de préparation.")
        return None, None, None

def semantic_search(query, model, index, k=50):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector, dtype=np.float32), k)
    return articles_df.iloc[indices[0]]

model = load_model()
index = load_faiss_index()
articles_df, authors_df, links_df = load_data()

if 'results_df' not in st.session_state:
    st.session_state.results_df = pd.DataFrame()
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

st.title("🤖 Chatbot Intelligent pour la Recherche sur Scopus")

if index is not None and articles_df is not None:
    st.sidebar.header("Filtres & Options")
    if st.sidebar.button("Effacer les résultats et la requête"):
        st.session_state.results_df = pd.DataFrame()
        st.session_state.last_query = ""
        st.rerun() 
    if user_query := st.chat_input("Posez une question (ENG) sur un sujet scientifique..."):
        st.session_state.results_df = semantic_search(user_query, model, index)
        st.session_state.last_query = user_query
    if st.session_state.last_query:
        st.markdown(f'<div class="user-message-container"><div class="user-message">{st.session_state.last_query}</div></div>', unsafe_allow_html=True)
    if not st.session_state.results_df.empty:
        results_to_filter = st.session_state.results_df
        result_article_ids = results_to_filter['article_id']
        result_author_ids = links_df[links_df['article_id'].isin(result_article_ids)]['author_id']
        authors_in_results = authors_df[authors_df['author_id'].isin(result_author_ids)]['author_name'].sort_values().unique()

        min_year = int(results_to_filter['year'].min())
        max_year = int(results_to_filter['year'].max())
        st.sidebar.subheader("Affiner les résultats actuels")

        if min_year == max_year:
            st.sidebar.write(f"Année de publication : {min_year}")
            year_range = (min_year, max_year)
        else:
            year_range = st.sidebar.slider(
                "Filtrer par année",
                min_year,
                max_year,
                (min_year, max_year)
            )
        
        selected_authors = []
        if len(authors_in_results) > 0:
            selected_authors = st.sidebar.multiselect(
                "Filtrer par Auteurs dans les résultats",
                options=authors_in_results
            )

        filtered_df = results_to_filter[
            (results_to_filter['year'] >= year_range[0]) & (results_to_filter['year'] <= year_range[1])
        ]

        if selected_authors:
            author_ids_to_filter = authors_df[authors_df['author_name'].isin(selected_authors)]['author_id']
            article_ids_to_keep = links_df[links_df['author_id'].isin(author_ids_to_filter)]['article_id']
            filtered_df = filtered_df[filtered_df['article_id'].isin(article_ids_to_keep)]
        
        with st.chat_message("assistant"):
            st.write(f"Affichage de **{len(filtered_df)}** résultats pertinents :")
            
            show_chart = st.sidebar.toggle("Afficher la distribution par année", value=False)
            if show_chart and not filtered_df.empty:
                st.subheader("Distribution des articles par année")
                year_counts = filtered_df['year'].value_counts().sort_index()
                fig = px.bar(year_counts, x=year_counts.index, y=year_counts.values, labels={'x':'Année', 'y':"Nombre d'articles"})
                st.plotly_chart(fig, use_container_width=True)

            if not filtered_df.empty:
                st.subheader("Articles correspondants")
                for _, row in filtered_df.iterrows():
                    with st.container(border=True):
                        st.markdown(f"#### {row['title']}")
                        author_names = links_df[links_df['article_id'] == row['article_id']].merge(authors_df, on='author_id')['author_name'].tolist()
                        st.markdown(f"**Auteurs :** {', '.join(author_names)}")
                        st.markdown(f"**Publication :** {row['publication_name']}  **Année :** {row['year']}")
                        st.markdown(f"**DOI :** [{row['doi']}](https://doi.org/{row['doi']})")
                        with st.expander("Voir le résumé"):
                            st.write(row['abstract'])
            else:
                st.warning("Aucun article ne correspond à vos critères de filtrage.")

else:
    st.warning("Les fichiers de données ne sont pas trouvés ou aucun sujet n'a été recherché. Veuillez poser une question.")