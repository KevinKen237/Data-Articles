import streamlit as st
import utilities_function as uf
import model
import itertools as it
import plotly.express as px
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
    # init état partagé
    st.session_state.setdefault("active_topic", None)
    # Main title and introduction
    st.markdown('<h1 class="main-title">📊 Data Science Blog Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: center;">by Kevin</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Découvrez, explorez et apprenez avec nos articles de data science</p>', unsafe_allow_html=True)
    

    # Navigation tabs
    tab1, tab2, tab3 = st.tabs([
        "🏠 Accueil", 
        "🔍 Recherche d'Articles", 
        "🤖 Recommandations"
    ])

    with tab1:
        home_page()
    
    with tab2:
        search_articles()
    
    with tab3:
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

@st.cache_data(ttl=600)
def get_recos(query, topic=None):
    return uf.systèmes_de_recommandation(query, topic=topic)

@st.cache_data(ttl=3600)
def resum(text):
    return model.resume_article_stream(text)


def render_reco(items):
    # items = liste de dicts {title, text, topic, url}
    for i, itx in enumerate(items):
        with st.container(border=True):
            st.caption(f"Topic : {itx['topic'].replace('_', ' ')}")
            st.markdown(f"**{itx['title']}**")
            st.markdown(resum(itx['text']))  # si coûteux, cf. cache ci-dessous
            st.markdown(f"[Lire l'article]({itx['url']})")
            # st.divider()  # si tu veux séparer visuellement
            
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
            st.session_state["active_topic"] = category.replace(" ","_")
            
    # Affichage du texte après avoir reçu l'entrée de l'utilisateur sur search_query
    if search_query:
        st.subheader("Articles recommandés")

        with st.spinner("Articles résumés par une IA en cours de génération..."):
            # Prépare le topic si filtre
            topic_kw = None if category == "Tous les Topics" else category.replace(' ', '_')

            try:
                titres, textes, topics, liens = get_recos(
                    search_query, topic=topic_kw
                )
                # ✅ Met à jour l’état global → l’onglet Recommandations se filtrera tout seul
                st.session_state["active_topic"] = topics[0] #if topics else None
            except Exception as e:
                st.error(f"Erreur lors de la recommandation : {e}")
            else:
                # Sécurise le zippage même si longueurs inégales (tu peux aussi exiger l'égalité)
                zipped = it.zip_longest(titres, textes, topics, liens, fillvalue="")
                items = [
                    {"title": t, "text": x, "topic": tp, "url": u}
                    for t, x, tp, u in zipped
                    if isinstance(x, str) and x.strip()  # ignore textes vides/NaN
                ]
                if not items:
                    st.info("Aucune recommandation exploitable.")
                else:
                    render_reco(items)
                # (option) rafraîchir tout de suite pour refléter le filtre si les onglets sont sur la même page :
                # st.rerun()
    


def to_items(titres, textes, topics, liens):
    # sécurise les longueurs et les types
    zipped = it.zip_longest(titres, textes, topics, liens, fillvalue="")
    items = []
    for t, x, tp, u in zipped:
        if isinstance(t, str) and isinstance(tp, str) and isinstance(u, str) and t and tp and u:
            items.append({"title": t.strip(), "text": str(x) if x is not None else "", "topic": tp.strip(), "url": u.strip()})
    return items

def render_topic_card(item):
    with st.container(border=True):
        st.caption(f"Topic : **{item['topic'].replace('_', ' ')}**")
        st.markdown(f"**{item['title']}**")
        st.markdown(f"[Ouvrir l’article]({item['url']})")

def render_topic_section(topic_name, items):
    st.subheader(topic_name.replace('_', ' '))
    for itx in items:
        render_topic_card(itx)

# ---------- Onglet 1 : Recommandations ----------
def recommendations():
    """Onglet de recommandations personnalisées"""
    st.header("🤖 Recommandations Personnalisées")

    # état partagé : topic actif décidé par la recherche
    active_topic = st.session_state.get("active_topic")
    if not active_topic:  # couvre None, '', etc.
        active_topic = None

    # Choix: tout ou filtré sur active_topic
    if active_topic:
        st.info(f"Filtre actif : **{active_topic.replace('_', ' ')}** (défini depuis l’onglet Recherche)")
        # On demande des recos pour CE topic
        titres, textes, topics, liens = uf.systèmes_de_recommandation(active_topic, topic=active_topic)
        items = to_items(titres, textes, topics, liens)
        if not items:
            st.warning("Aucune recommandation pour ce topic.")
            return
        render_topic_section(active_topic, items)
        if st.button("❌ Effacer le filtre", key="clear_filter"):
            st.session_state["active_topic"] = None
            st.success("Impossible car recherche d'article toujours en cours")
            st.rerun()
            
            
    else:
        st.caption("Aucun filtre actif. Affichage par topics.")
        # Exemple: afficher N topics populaires (à adapter à ton projet)
        topics_liste = get_topics_names()  # <-- remplace par ta source de topics
        for tp in topics_liste:
            titres, textes, topics, liens = uf.systèmes_de_recommandation(tp, topic=tp)
            items = to_items(titres, textes, topics, liens)
            if items:
                render_topic_section(tp, items[:5])

# Point d'entrée principal
if __name__ == "__main__":
    main()
