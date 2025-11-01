from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from load_treat_data import get_topics_names, clean_text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import time



def word_cloud_all():
    with open('data/word_count/word_all_articles.json') as json_file:
        dic = json.load(json_file)
    x,y = np.ogrid[:400,:400]
    mask = (x-200)**2 + (y-200)**2 > 160**2
    mask = 255 * mask.astype(int)
    
    wordcloud = WordCloud(background_color="white", mask=mask, contour_width=3,
                            contour_color="black", max_font_size=170, random_state=42,
                            colormap="Dark2").generate_from_frequencies(dic)
    plt.subplots(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    # Donner un titre à la figure
    plt.title(f"Word of DATA", fontsize=16)
    plt.axis('off')  # Désactiver les axes
    return plt

def word_cloud_topic(topic):
    with open('data/word_count/word_count.json') as json_file:
        dic = json.load(json_file)
        
    # On filtre le dictionnaire pour ne garder que les mots du topic
    dic = dic[topic]
    x,y = np.ogrid[:400,:400]
    mask = (x-200)**2 + (y-200)**2 > 160**2
    mask = 255 * mask.astype(int)
    
    wordcloud = WordCloud(background_color="white", mask=mask, contour_width=3,
                            contour_color="black", max_font_size=170, random_state=42,
                            colormap="Dark2").generate_from_frequencies(dic)
    plt.subplots(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    # Donner un titre à la figure
    plt.title(f"{topic.replace('_','' '')}", fontsize=16)
    plt.axis('off')  # Désactiver les axes
    return plt

def volume_articles():
    topics = get_topics_names()
    volume = []
    for topic in topics:
        df = pd.read_csv(f'data/processed/{topic}_processed.csv')
        volume.append(len(df))
    # On crée un DataFrame avec les topics et le volume d'articles
    volume = pd.DataFrame({'Topics': topics, 'Volume': volume})
    return volume

def total_articles():
    df = pd.read_csv('data/all_articles.csv')
    return len(df)

def filter_topic(topic):
    df = pd.read_csv('data/all_articles.csv')
    # On filtre le dataframe pour ne garder que les lignes avec "topic" dans la colonne "topic"
    df = df[df['topic'] == topic]
    return df

def systèmes_de_recommandation(query, topic=None):
    debut = time.time()
    #print(topic)
    if topic:
        df = filter_topic(topic)
    else:
        df = pd.read_csv('data/all_articles.csv')
       
    # On commence par mettre dans une liste (nos documents) les textes des articles
    documents = df.Texte_clean.fillna('').astype(str).str.strip().tolist()
    
    # On vectorise les documents
    vectorizer2 = TfidfVectorizer(lowercase=True, stop_words=None,
                                ngram_range=(1, 1),
                                use_idf=True, smooth_idf=True,
                                sublinear_tf=False, norm='l2')

    dtm = vectorizer2.fit_transform(documents)
    
    # On effectue le prétraitement de la requête
    query = clean_text(query)
    # On vectorise la requête
    requete_vect = vectorizer2.transform([query])
    # On calcule la similarité cosinus entre la requête et les documents
    cos_sim = cosine_similarity(requete_vect, dtm)
    # On récupère les 2 indices des documents les plus similaires
    indices = cos_sim.argsort(axis=None)[::-1][:2]
    # On retourne les 3 articles les plus similaires (titre et texte)
    titre = [df.iloc[i].Titre for i in indices]
    texte = [df.iloc[i].Texte for i in indices]
    topic = [df.iloc[i].topic for i in indices]
    lien = [df.iloc[i].Liens for i in indices]  
    fin = time.time()
    print(f"Temps d'exécution système de recommandation : {fin - debut} secondes")
    return titre, texte, topic, lien
    