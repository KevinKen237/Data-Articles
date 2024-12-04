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
    return wordcloud

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
    return wordcloud

def volume_articles():
    topics = get_topics_names()
    volume = {}
    for topic in topics:
        df = pd.read_pickle(f'data/processed/{topic}_processed.pkl')
        volume[topic] = len(df)
    return volume

def total_articles():
    df = pd.read_pickle('data/all_articles.pkl')
    return len(df)

print(volume_articles())    