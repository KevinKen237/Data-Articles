# Dans ce fichier, nous allons scrapper les données et les stocker dans différents fichiers

# Importation des librairies
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time
import sys


# Fonction pour récupérer le contenu html d'une page web
def get_bsobj_from_url(mon_url):
    time.sleep(random.uniform(0.4, 1))
    # Ouvrir avec openurl mon_url
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(mon_url,headers={'User-Agent':user_agent})

    try: # gestion des exceptions avec un bloc try/except
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e) # sortie du programme avec affichage de l’erreur
    bsobj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml
    return bsobj

# Fonction pour récupérer les liens des topics et les titres
def get_topics_info(url):
    url = url + "topic"
    bsobj = get_bsobj_from_url(url)
    topics = bsobj.findAll("li", class_="li-has-thumb")
    topic_links = []
    topic_titles = []
    for topic in topics:
        topic_links.append(topic.find("a").get("href"))
        topic_titles.append(topic.find("b").get_text())
    return topic_titles, topic_links

#print(get_topics_info(("https://www.kdnuggets.com/")))

# Fonction pour récupérer les liens des articles d'un topic et son titre
def get_article_info(url):
    bsobj = get_bsobj_from_url(url)
    articles = bsobj.find("ul", class_ = "three_ul").find_all("li")
    article_links = []
    article_titles = []
    for article in articles:
        article_links.append(article.find("a").get("href"))
        article_titles.append(article.find("b").get_text())
    return article_titles, article_links