# Dans ce fichier, nous récupérons les données scrappées et les traitons pour les stocker dans un fichier csv 

# Importation des librairies
import pandas as pd
import os
from functools import reduce
import csv
import spacy
import re
from unidecode import unidecode
import string
from nltk.stem import PorterStemmer

# Augmentez la limite de taille des champs
csv.field_size_limit(10**9)

pd.set_option('display.max_colwidth', None)  # Afficher les colonnes en entier
pd.set_option('display.max_rows', None)     # Afficher toutes les lignes (si nécessaire)
# Une alternative peut être d'utiliser des fichiers pickle pour sauvregarder nos documents

#!python -m spacy download en_core_web_sm

def get_topics_names():
    # On récupère les noms des dossiers dans data
    repository = "data"
    topics = [f for f in os.listdir(repository) if os.path.isdir(os.path.join(repository, f))]
    return topics


def load_topic(name):
   return pd.read_csv(f"data/{name}/articles.csv", sep=",", header=0, encoding='utf-8', quoting=csv.QUOTE_MINIMAL, index_col=False)

def load_all_topics():
    topics = get_topics_names()
    # On charge les dataframes de chaque topic a l'aide de map
    dfs = list(map(load_topic, topics))
    # On concatène les dataframes
    df = reduce(lambda x, y: pd.concat([x, y]), dfs)
    
    return df

df = load_all_topics()

def racinisation(text):
    stemmer = PorterStemmer()
    # On tokenise le texte
    tokens = text.split()
    # On applique la racinisation
    text = ' '.join([stemmer.stem(token) for token in tokens])
    return text

def clean_text(text):
    nlp = spacy.load('en_core_web_sm')
    # Suppression des accents
    text = unidecode(text)
    # Suppression de la ponctuation
    for punct in string.punctuation.replace('-', ''):
        text = text.replace(punct, '')
    text = text.lower().replace("\xa0 \xa0\n", "")
    # Suppression des espaces en trop
    text = re.sub(r'\s+', ' ', text) 
    #Suppression des chiffres
    text = re.sub(r'\d+', '', text) 
    # Gestion des url
    text = re.sub(r'https?:\S+', "URLEXPR", text) # http://t.co/eFKkE9W0GI
    text = re.sub(r'\bwww\.\S+', "URLEXPR", text) # www.example.com
    # Suppression des stopwords, caractères spéciaux avec spacy
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]  
    text = ' '.join(tokens)
    return text 

print(clean_text(str(df.Texte[0])))