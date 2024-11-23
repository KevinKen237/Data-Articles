# Dans ce fichier, nous récupérons les données scrappées et les traitons pour les stocker dans un fichier csv 

# Importation des librairies
import pandas as pd
import os

def get_topics_names():
    # On récupère les noms des dossiers dans data
    repository = "data"
    topics = [f for f in os.listdir(repository) if os.path.isdir(os.path.join(repository, f))]
    return topics