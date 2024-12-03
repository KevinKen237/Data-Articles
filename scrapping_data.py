# Dans ce fichier, nous allons scrapper les données et les stocker dans différents fichiers

# Importation des librairies
# ! pip install requierments.txt
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time
import sys
import dask
import pandas as pd
from pathlib import Path


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

#print(get_article_info("https://www.kdnuggets.com/tag/data-science"))

def extract_text(url):
    try:
        soup = get_bsobj_from_url(url)
        texte = []
        for p in soup.find("div", id="post-").find_all('p'):
            texte.append(p.get_text())
        texte = ' '.join(texte)
        return texte
    except Exception as e:
        return f"Error extracting text from {url}: {str(e)}"

# Fonction qui a partir d'un lien de page, crée un dossier pour un topic puis un fichier csv avec en première colonne le titre de l'article et en deuxième colonne le texte de l'article
def save_articles(topic_title, topic_link):
    topic_folder = topic_title.replace(" ", "_")
    path = Path(f'data/raw')
    # On vérifie si le dossier existe déjà et ce n'est pas le cas on le crée
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
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
    df = pd.DataFrame({'Titre': article_titles, 'Texte': articles})
    # On sauvegarde le dataframe dans un fichier csv
    df.to_pickle(f'{path}/{topic_folder}_raw.pkl')
    print(f'{topic_title} saved')
    
#save_articles("Data Science", "https://www.kdnuggets.com/tag/data-science")

# Fonction qui à partir d'un lien de page, crée un dossier pour chaque topic et un fichier csv, en parallélisant avec dask

def save_articles_multiprocess(url):
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
   
# Scrapping: environ 9 minutes pour scraper les données de 12 topics


    