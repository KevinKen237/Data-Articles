from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from load_treat_data import get_topics_names


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
    plt.title(f"{topic.replace("_"," ")}", fontsize=16)
    plt.axis('off')  # Désactiver les axes
    return plt

def volume_articles():
    topics = get_topics_names()
    volume = []
    for topic in topics:
        df = pd.read_pickle(f'data/processed/{topic}_processed.pkl')
        volume.append(len(df))
    # On crée un DataFrame avec les topics et le volume d'articles
    volume = pd.DataFrame({'Topics': topics, 'Volume': volume})
    return volume

def total_articles():
    df = pd.read_pickle('data/all_articles.pkl')
    return len(df)

def filter_topic(topic):
    df = pd.read_pickle(f'data/all_articles.pkl')
    return df

