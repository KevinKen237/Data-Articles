''' Dans ce fichier, nous allons scrapper les données et les stocker dans différents fichiers '''

# Importation des librairies
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time, socket
import sys
import dask
import pandas as pd
from pathlib import Path


# Fonction pour récupérer le contenu html d'une page web
def get_bsobj_from_url(mon_url, *, timeout=15):
    #print("1")
    time.sleep(random.uniform(0.4, 1))
    # Ouvrir avec openurl mon_url
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    req = Request(mon_url,headers={'User-Agent':user_agent})

    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except HTTPError as e:
        # ex: 404 Not Found
        raise RuntimeError(f"HTTP {e.code} {e.reason} for {mon_url}") from e
    except URLError as e:
        raise RuntimeError(f"URL error for {mon_url}: {e.reason}") from e
    except socket.timeout as e:
        raise RuntimeError(f"Timeout fetching {mon_url}") from e

    try:
        return BeautifulSoup(data, "lxml")
    except Exception as e:
        raise RuntimeError(f"HTML parse error for {mon_url}: {e}") from e

# Fonction pour récupérer les liens des topics et les titres
def get_topics_info(url):
    #print("2")
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
    #print("3")
    bsobj = get_bsobj_from_url(url)
    articles = bsobj.find("ul", class_ = "three_ul").find_all("li")
    article_links = []
    article_titles = []
    for article in articles:
        article_links.append(article.find("a").get("href"))
        article_titles.append(article.find("b").get_text())
    return article_titles, article_links

#print(get_article_info("https://www.kdnuggets.com/tag/data-science"))

def extract_text(url):
    #print("4")
    try:
        soup = get_bsobj_from_url(url)
        texte = []
        for p in soup.find("div", id=re.compile(r"^post-")).find_all('p'):
            if not p:
                return f"Error extracting text from {url}: no paragraphs found"
            texte.append(p.get_text())
        texte = ' '.join(texte)
        return texte
    except Exception as e:
        return f"Error extracting text from {url}: {str(e)}"

# Fonction qui a partir d'un lien de page, crée un dossier pour un topic puis un fichier csv avec en première colonne le titre de l'article et en deuxième colonne le texte de l'article
def save_articles(topic_title, topic_link):
    print("5")
    topic_folder = topic_title.replace(" ", "_")
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    # On récupère les liens des articles
    article_titles, article_links = get_article_info(topic_link)
    # On construit un dataframe avec les titres et les textes des articles
    articles = []
    
    batch_size = 10  # On crée des batchs de 10 articles pour éviter de surcharger le serveur lors du dask.compute
    for i in range(0, len(article_links), batch_size):
        batch_links = article_links[i:i+batch_size]
        batch_tasks = [dask.delayed(extract_text)(link) for link in batch_links]   # On parallelise l'extraction du texte des articles car il y'en a pleins
        batch_results = dask.compute(*batch_tasks)
        articles.extend(batch_results)
    df = pd.DataFrame({'Titre': article_titles, 'Texte': articles, 'Liens': article_links})
    # On sauvegarde le dataframe dans un fichier csv
    df.to_csv(f'{path}/{topic_folder}_raw.csv', index=False)
    print(f'{topic_title} saved')
    
#save_articles("Data Science", "https://www.kdnuggets.com/tag/artificial-intelligence")

# Fonction qui à partir d'un lien de page, crée un dossier pour chaque topic et un fichier csv, en parallélisant avec dask

def save_articles_multiprocess(url):
    #print("6")
    topic_titles, topic_links = get_topics_info(url)
    tasks = [dask.delayed(save_articles)(title, link) for title, link in zip(topic_titles, topic_links)] # pas conseillé de faire un map dans ce car save_articles en utilise déja et est appelé encore ici en dask.delayed
    # Exécution des tâches en parallèle
    dask.compute(*tasks)   

def main():
    url = "https://www.kdnuggets.com/"
    save_articles_multiprocess(url)
    

if __name__ == "__main__":  
   from dask.distributed import Client
   client = Client(timeout="30s", n_workers=4)   # Création d'un cluster de 4 workers. timeout de 30s permet de ne pas avoir de timeout lors de l'exécution des tâches
   main()   
   client.close()