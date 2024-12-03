# Dans ce fichier, nous récupérons les données scrappées et les traitons pour les stocker dans un fichier csv 

# Importation des librairies
import pandas as pd
import os
from functools import reduce
import spacy
import re
from unidecode import unidecode
import string
from nltk.stem import PorterStemmer
import dask.dataframe as dd
from pathlib import Path
from dask.distributed import Client



pd.set_option('display.max_colwidth', None)  # Afficher les colonnes en entier
pd.set_option('display.max_rows', None)     # Afficher toutes les lignes (si nécessaire)
# Une alternative peut être d'utiliser des fichiers pickle pour sauvregarder nos documents

#!python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

def get_topics_names(repository = "data/raw"):
    # récupérons les noms des fichiers dans repository et supprimons la pratie "_raw.pkl"
    topics = [f.replace("_raw.pkl", "") for f in os.listdir(repository)]
    return topics

# Charger un topic spécifique
def load_topic(name,id):
   return pd.read_pickle(f"data/{id}/{name}_{id}.pkl")

# Sauvegarder un topic spécifique
def save_topic(name, df):
    df.to_pickle(f"data/processed/{name}_processed.pkl")

def load_all_topics(id):
    topics = get_topics_names()
    # On charge les dataframes de chaque topic a l'aide de map
    dfs = list(map(load_topic, topics,id))
    # On concatène les dataframes
    df = reduce(lambda x, y: pd.concat([x, y]), dfs)
    
    return df


def racinisation(text):
    stemmer = PorterStemmer()
    # On tokenise le texte
    tokens = text.split()
    # On applique la racinisation
    text = ' '.join([stemmer.stem(token) for token in tokens])
    return text

def clean_text(text):
    # Suppression des accents
    text = str(text)
    text = unidecode(text)
    
    # Suppression des espaces en trop
    text = re.sub(r'\s+', ' ', text) 
    #Suppression des chiffres
    text = re.sub(r'\d+', '', text) 
    # Gestion des url
    text = re.sub(r'https?:\S+', "URLEXPR", text) # http://t.co/eFKkE9W0GI
    text = re.sub(r'\bwww\.\S+', "URLEXPR", text) # www.example.com
    
    # Suppression de la ponctuation sauf le tiret
    for punct in string.punctuation.replace('-', ''):
        text = text.replace(punct, '')
    text = text.lower().replace("\xa0 \xa0\n", "")
    
    # Suppression des stopwords, caractères spéciaux avec spacy
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]  
    text = ' '.join(tokens)
    return text 

def clean_text_and_racinise(text):
    clean = clean_text(str(text))
    return racinisation(clean)

#print(racinisation(clean_text(str(df.Texte[0]))))

# Fonction de nettoyage des données en parallélisant le traitement
def clean_data(name):
    df = load_topic(name, "raw")
    # Convertir le DataFrame en DataFrame Dask car il est plus rapide pour le traitement en parallèle
    ddf = dd.from_pandas(df, npartitions=10)
    # Appliquer les opérations sur une colonne
    ddf = ddf.assign(
    Texte_clean=lambda df: df['Titre'].map(clean_text, meta=('Texte', 'str')),
    Texte_clean_racine=lambda df: df['Texte'].map(clean_text_and_racinise, meta=('Texte', 'str'))
    )
    # Retourner un DataFrame pandas après traitement
    ddf = ddf.compute()
    # On sauvegarde le dataframe dans un fichier pkl
    save_topic(name, ddf)
    print(f'{name} cleaned and saved')


def clean_all_data():
    topics = get_topics_names()
    path = Path(f'data/processed')
    # On vérifie si le dossier existe déjà et ce n'est pas le cas on le crée
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    # On nettoie les données de chaque topic avec un map
    list(map(clean_data, topics))
    
        
    

#print(clean_data(df).head())

def main():
    clean_all_data()
    
if __name__ == "__main__":  
   client = Client(timeout="30s", n_workers=4)   # Création d'un cluster de 4 workers. timeout de 30s permet de ne pas avoir de timeout lors de l'exécution des tâches
   main()