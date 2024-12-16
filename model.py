# Importation des librairies nécessaires
#from transformers import pipeline
import subprocess
import time
import streamlit as st
#import os
#os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
"""
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# Charger le modèle LED fine-tuné sur arXiv
summarizer = pipeline("summarization", model="allenai/led-large-16384-arxiv")

def get_summary(text):
    input_length = len(text.split())  # Longueur approximative en tokens
    max_length = min(130, int(input_length * 0.5))  # 50% de la longueur d'entrée
    min_length = min(30, int(input_length * 0.25))  # 25% de la longueur d'entrée
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

    
#print(get_summary("The EU AI Act recently entered into force. It is one of the most comprehensive frameworks that has set precedence on making the best use of cutting-edge innovation. The “best use” needs more attention here — it underscores the importance of responsible development, deployment, and utilization of AI systems.\
#Ethics is not just limited to the European Union, it is also the core focus of the US. A recent White House announcement promotes using concrete safeguards in AI to ensure the rights or safety of everyone involved. In line with the announcement, the role of Chief AI Officers is introduced to manage the risks associated with AI."))
"""

# Model de résumé utilisant mistral en local à la place de Hugging Face; cela permet de réduire le temps de réponse et on a de meilleurs résultats
@st.cache_data
def resume_article(text):
    debut = time.time()
    # Construire la commande pour appeler Mistral en ligne de commande via 'ollama chat'
    command = ["ollama", "run", "mistral"]
    prompt_text = "Summarize in 50 words:\n" + text
    # Utiliser subprocess pour exécuter la commande, envoyer le texte en entrée et récupérer la sortie
    try:
    # Lancer la commande et fournir le prompt en tant qu'entrée
        result = subprocess.run(command, input=prompt_text, text=True,
        capture_output=True, check=True)
        fin = time.time()
        print(f"Temps d'exécution du résumé : {fin - debut} secondes")
        # Récupérer et retourner la sortie du modèle
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Gérer les erreurs éventuelles
        print(f"Erreur lors de l'exécution de Mistral : {e}")
        return None
    
#print(run_mistral_with_text("Dask is a powerful Python library. It is open-source and free. Dask is designed for parallel computing. This means it can run many tasks at the same time. It helps process large datasets that don’t fit in memory. Dask splits these large datasets into smaller parts. These parts are called chunks. Each chunk is processed separately and in parallel. This speeds up the process of handling big data.\
#Dask works well with popular Python libraries. These include NumPy, Pandas, and Scikit-learn. Dask helps these libraries work with larger datasets. It makes them more efficient. Dask can run on one computer or multiple computers. It can scale from small tasks to large-scale data processing. Dask is easy to use. It fits well into existing Python workflows. Data scientists use Dask to handle big data without issues. It removes the limitations of memory and computation speed."))