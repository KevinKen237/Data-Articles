import httpx
import time, ollama
import streamlit as st
import os

# on crée un client Ollama lié à l'URL du service docker "ollama"
def _make_client():
    # URL interne Docker vers le service Ollama
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    # selon la version du package ollama, l'argument du client change.
    # on essaie d'abord 'host', puis on retombe sur 'base_url'.
    try:
        return ollama.Client(host=base_url)
    except TypeError:
        return ollama.Client(base_url=base_url)

ollama_client = _make_client()

def resume_article_stream(text: str, max_words: int = 150):
    prompt = (
        f"Génère un article en ≤ {max_words} à partir du texte ci-dessous. Sans titre. Objectif: susciter l'intérêt du lecteur.\n\n"
        f"{text}\n"
    )

    words = []
    container = st.empty()
    try:
        for chunk in ollama_client.generate(
            model="mistral:instruct",
            prompt=prompt,
            options={"num_predict": 180, "temperature": 0.7},
            stream=True,
        ):
            
            part = chunk.get("response", "")
            if part is None:
                break
            
            words.append(part)
            container.markdown("".join(words))
            time.sleep(0.01)  # léger délai pour un rendu fluide
        #return "".join(words)
    except httpx.ConnectError:
        container.markdown(
        "⚠️ _résumé indisponible pour le moment (serveur IA occupé)_"
        )
    except Exception as e:
        container.markdown(
        f"Erreur IA lors du résumé : {e}"
        )

    
