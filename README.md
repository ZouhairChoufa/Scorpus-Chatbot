# Moteur de Recherche Sémantique pour Articles Scientifiques

Ce projet est une application web interactive qui permet de faire de la recherche sémantique dans une base de données d'articles scientifiques extraits de l'API Scopus. Contrairement à une recherche par mot-clé classique, ce moteur de recherche utilise un modèle d'intelligence artificielle pour comprendre le sens de la requête de l'utilisateur et trouver les articles les plus pertinents.

L'interface, développée avec Streamlit, est conçue comme un chatbot où l'utilisateur peut poser une question en langage naturel pour trouver des articles, puis affiner les résultats grâce à des filtres dynamiques.

##  Fonctionnalités

* **Recherche Sémantique** : Utilise des vecteurs sémantiques (embeddings) pour trouver des correspondances basées sur le sens plutôt que sur les mots-clés exacts.
* **Interface Chatbot** : Une interface utilisateur simple et moderne pour poser des questions.
* **Extraction de Données** : Un script pour extraire des données sur n'importe quel thème depuis l'API Scopus.
* **Filtres Dynamiques** : Affinez les résultats de la recherche par année de publication et par auteur.
* **Visualisation de Données** : Affichez un graphique interactif de la distribution des articles par année.
* **Accès Facile aux Informations** : Liens directs vers les articles via leur DOI et résumés consultables dans un menu déroulant.

##  Structure du Projet

Le projet est organisé en plusieurs scripts qui doivent être exécutés dans un ordre précis :

* `requirements.txt` : La liste de toutes les dépendances Python nécessaires au projet.
* `.env` (à créer) : Fichier de configuration pour stocker les clés d'API secrètes.
* `extract_data.py` : Script pour interroger l'API Scopus et télécharger les données brutes des articles.
* `clean_and_store.py` : Script pour nettoyer les données brutes, les normaliser et les sauvegarder dans des fichiers CSV propres.
* `create_index.py` : Script qui transforme les résumés des articles en vecteurs sémantiques et crée un index de recherche rapide avec FAISS.
* `app.py` : Le script principal qui lance l'application web interactive avec Streamlit.

##  Installation

Suivez ces étapes pour configurer l'environnement du projet.

1.  **Cloner le projet** (si ce n'est pas déjà fait) et naviguez dans le dossier :
    ```bash
    git clone <url-de-votre-projet>
    cd <nom-du-dossier-du-projet>
    ```

2.  **Créer et activer un environnement virtuel** :
    ```bash
    # Pour Windows
    python -m venv venv
    venv\Scripts\activate

    # Pour macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installer les dépendances** à partir du fichier `requirements.txt` :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer les clés d'API** :
    * Créez un fichier nommé `.env` à la racine du projet.
    * Ajoutez vos clés Scopus à l'intérieur :
        ```env
        SCOPUS_API_KEY="VOTRE_CLE_API_PERSONNELLE_ICI"
        SCOPUS_INST_TOKEN="VOTRE_JETON_INSTITUTIONNEL_ICI"
        ```

##  Utilisation

Les scripts doivent être exécutés dans l'ordre suivant pour que l'application fonctionne correctement.

1.  **Étape 1 : Extraire les données**
    * Lancez ce script pour télécharger les données brutes. Le terminal vous demandera d'entrer un thème de recherche.
    * Vous pouvez exécuter ce script plusieurs fois avec différents thèmes pour enrichir votre base de données. Cela créera un fichier *_raw.json pour chaque thème recherché.
    ```bash
    python extract_data.py
    ```

2.  **Étape 2 : Nettoyer les données**
    * Ce script traite tous les fichiers `*_raw.json` et les sauvegarde dans des fichiers CSV `articles.csv, authors.csv, et article_author_links.csv` propres.
    ```bash
    python clean_and_store.py
    ```

3.  **Étape 3 : Créer l'index de recherche**
    * Ce script lit `articles.csv` et crée le fichier `articles.index`( l'index sémantique FAISS ) pour la recherche rapide.
    ```bash
    python create_index.py
    ```

4.  **Étape 4 : Lancer l'application web**
    * Démarrez l'interface utilisateur interactive avec Streamlit.
    ```bash
    streamlit run app.py
    ```
    * Ouvrez votre navigateur à l'adresse locale affichée (généralement `http://localhost:8501`).

##  Technologies Utilisées

* **Langage** : Python 3.x
* **Manipulation de données** : Pandas
* **Interaction API** : Requests, Scopus API
* **Machine Learning / IA** :
    * `sentence-transformers` pour la vectorisation sémantique.
    * `faiss` (de Meta AI) pour l'indexation et la recherche de similarité.
* **Interface Web** : Streamlit
* **Visualisation** : Plotly