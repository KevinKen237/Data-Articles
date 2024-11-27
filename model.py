# Dans cette partie, nous allons effectuer une lda sur nos données

# Importation des librairies nécessaires
#from gensim import corpora, models
#import gensim
import load_treat_data
import pandas as pd

# Préparation avant lancement de la LDA, il nous faut créer deux objets gensim
#    (*) un objet dictionary qui comprend tous les mots utilisés dans l'ensemble des topics abordés
#    (*) un objet corpus (document term matrix) qui contient tous les topics mais sous
#    la forme de vecteurs dont les éléments sont des 1s ou des 0s. 1 si le mot est
#    présent dans le topic. 0 sinon.

def get_list_topic_text():
    list_texte = []
    topics = load_treat_data.get_topics_names()
    for topic in topics:
        df = pd.read_pickle(f"data/{topic}/articles")
        list_texte.append(df["Texte"])
    return list_texte

df = pd.read_pickle("clean_data.pkl")
print(df.head(1))