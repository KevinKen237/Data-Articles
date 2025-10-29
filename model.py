import time, ollama
import streamlit as st


def resume_article_stream(text: str, max_words: int = 80):
    prompt = (
        f"Génère un article en ≤ {max_words} à partir du texte ci-dessous. Sans titre.\n\n"
        f"{text}\n"
    )

    words = []
    container = st.empty()
    for chunk in ollama.generate(
        model="mistral:instruct",
        prompt=prompt,
        options={"num_predict": 130, "temperature": 0.7},
        stream=True,
    ):
        part = chunk.get("response", "")
        if part is None:
            break
        
        words.append(part)
        container.markdown("".join(words))
        time.sleep(0.01)  # léger délai pour un rendu fluide
    #return "".join(words)

    
