import streamlit as st
import pandas as pd
import utilities_function as uf
import plotly.express as px
#import matplotlib.pyplot as plt
from load_treat_data import get_topics_names

#import plotly.graph_objs as go
topics = get_topics_names()
# Page configuration
st.set_page_config(
    page_title="Data Science Blog Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    color: #2C3E50;
    text-align: center;
    margin-bottom: 30px;
}
.subtitle {
    font-size: 20px;
    color: #7F8C8D;
    text-align: center;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

def main():
    # Main title and introduction
    st.markdown('<h1 class="main-title">📊 Data Science Blog Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: center;">by Kevin</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Découvrez, explorez et apprenez avec nos articles de data science</p>', unsafe_allow_html=True)
    

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Accueil", 
        "🔍 Recherche d'Articles", 
        "📈 Tendances", 
        "🤖 Recommandations"
    ])

    with tab1:
        home_page()
    
    with tab2:
        search_articles()
    
    with tab3:
        trends_visualization()
    
    with tab4:
        recommendations()

def home_page():
    """Page d'accueil avec présentation du projet"""
    st.header("Bienvenue sur notre Blog de Data Science")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("À propos du Projet")
        st.markdown("""
        Ce blog interactif est votre plateforme pour explorer des articles de data science :
        - **ETL Avancé** : Sujets soigneusement sélectionnés, nettoyées et mis à jour chaque semaine
        - **Recherche Intuitive** : Trouvez des articles par mots-clés
        - **Recommandations Personnalisées** : Découvrez de nouveaux contenus
        - **Visualisation des Tendances** : Comprenez l'évolution des topics
        """)
    
    with col2:
        st.subheader("Statistiques Rapides")
        # Placeholder for some quick stats
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Total Articles", f"{uf.total_articles()}+")
        with stats_col2:
            st.metric("Catégories", "12")
        
        # Sample pie chart of categories
        volume = uf.volume_articles()
        fig = px.bar(
        volume,
        x='Topics',
        y='Volume',
        title="Volume d'Articles par Catégorie",
        color='Topics',
        width=600,  # Largeur en pixels
        height=400  # Hauteur en pixels
                    )
        st.plotly_chart(fig, key="Volume d'articles")  # Affichage du graphique Plotly
        
    # Word cloud of all articles
    fig = uf.word_cloud_all()
    st.pyplot(fig)  # Afficher dans Streamlit


def search_articles():
    import model  # Ainsi, ce n'est que lorsque l'on est sur cet onglet que le modèle est chargé
    """Onglet de recherche d'articles"""
    st.header("🔍 Recherche d'Articles")
    
    # Placeholder for search functionality
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_query = st.text_input("Entrez des mots-clés ou des thèmes")
        st.write("Cela peut prendre quelques secondes pour afficher les résultats")
    
    with search_col2:
        topics0 = [topic.replace("_"," ") for topic in get_topics_names()]
        topics0.insert(0, "Tous les Topics")
        category = st.selectbox("Catégorie", 
            topics0
        )
        if category != "Tous les Topics":
            fig = uf.word_cloud_topic(category.replace(" ","_"))
            st.pyplot(fig)
            
    # Affichage du texte après avoir reçu l'entrée de l'utilisateur sur search_query
    if search_query:
        st.subheader("Recommandation")    
        if category == "Tous les Topics":
            print("il ne veut pas faire de filtre")
            titre_recom, texte_recom, topic_recom = uf.systèmes_de_recommandation(search_query)
            for i in range(len(titre_recom)):
                st.text_area(
                    label=f"Topic : {topic_recom[i].replace('_', ' ')}", 
                    value=f"Titre : {titre_recom[i]}\n\n{model.resume_article(texte_recom[i])}", 
                    height=300
                )
        else:
            print("il veut faire un filtre")
            titre_recom, texte_recom, topic_rec = uf.systèmes_de_recommandation(search_query, category)
            for i in range(len(titre_recom)):
                st.text_area(
                    label=f"Titre : {titre_recom[i]}", 
                    value=model.resume_article(texte_recom[i]), 
                    height=300
                )
    

def trends_visualization():
    """Onglet de visualisation des tendances"""
    st.header("📈 Tendances des Topics")
    volume = uf.volume_articles()
    fig2 = px.bar(
        volume,
        x='Topics',
        y='Volume',
        title="Volume d'Articles par Catégorie",
        color='Topics'
                    )
    st.plotly_chart(fig2, key="trends_volume")  # Affichage du graphique Plotly
    
    st.write("Visualisations des trends à développer")

def recommendations():
    """Onglet de recommandations personnalisées"""
    st.header("🤖 Recommandations Personnalisées")
    st.write("Moteur de recommandation à implémenter")

# Point d'entrée principal
if __name__ == "__main__":
    main()

# Notes pour le développement ultérieur :
# 1. Implémenter la logique de recherche avec filtrage
# 2. Développer le moteur de recommandation (TF-IDF/embeddings)
# 3. Créer des visualisations détaillées des tendances
# 4. Intégrer une base de données ou des fichiers CSV
# 5. Ajouter l'authentification si nécessaire
