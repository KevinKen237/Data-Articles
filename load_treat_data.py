# Dans ce fichier, nous récupérons les données scrappées et les traitons pour les stocker dans un fichier csv 

# Importation des librairies
import pandas as pd
import os
from functools import reduce

def get_topics_names():
    # On récupère les noms des dossiers dans data
    repository = "data"
    topics = [f for f in os.listdir(repository) if os.path.isdir(os.path.join(repository, f))]
    return topics


def load_topic(name):
   return pd.read_csv(f"projet/data/{name}/articles.csv", sep=",")

def load_all_topics():
    topics = get_topics_names()
    # On charge les dataframes de chaque topic a l'aide de map
    dfs = list(map(load_topic, topics))
    # On concatène les dataframes
    df = reduce(lambda x, y: pd.concat([x, y]), dfs)
    
    return df

df = load_all_topics()