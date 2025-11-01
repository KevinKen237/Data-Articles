# ---------------------------
# Dockerfile pour ton app Streamlit + Ollama local
# ---------------------------

# Image de base : Python 3.11 slim
FROM python:3.11-slim

# Eviter les .pyc et forcer l'affichage direct des logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY . .

# Exposer le port 8501 pour Streamlit
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]