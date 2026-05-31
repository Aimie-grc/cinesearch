import streamlit as st
from elasticsearch import Elasticsearch

from config import create_mapping
from indexer import index_movies
from search import (
    search_by_title,
    search_advanced,
    search_plot,
    search_fuzzy,
    suggest_titles
)
from analytics import (
    global_stats,
    top_genres,
    top_actors,
    top_directors,
    distribution,
    best_rated_directors,
    best_rated_genres,
    evolution_note
)

# ======================================
# CONFIG PAGE
# ======================================

st.set_page_config(
    page_title="CineSearch",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CineSearch")

# ======================================
# ES CONNECTION
# ======================================

@st.cache_resource
def get_es():
    es = Elasticsearch("http://localhost:9200")
    es.info()
    return es

st.sidebar.title("🎬 CineSearch")
try:
    es = get_es()
    st.sidebar.success("Elasticsearch connecté")

    if not es.indices.exists(index="movies"):
        st.sidebar.warning("Index 'movies' introuvable, création en cours")
        create_mapping(es)
        index_movies(es, "data/movies_cleaned_v2.json")

except Exception as e:
    st.error(f"Erreur connexion Elasticsearch : {e}")
    st.stop()


# ======================================
# UTILS (remplace format_result)
# ======================================

def display_results(results):

    if not results:
        st.warning("Aucun résultat trouvé.")
        return

    for i, item in enumerate(results, 1):

        title = (
            item.get("title")
            or item.get("name")
            or f"Résultat {i}"
        )

        with st.expander(f"{i}. {title}"):

            for key, value in item.items():

                if key in ["_id", "_index", "_score"]:
                    continue

                if isinstance(value, list):
                    value = ", ".join(map(str, value))

                elif isinstance(value, dict):
                    value = str(value)
                
                elif isinstance(value, float):
                    value = round(value,2)

                st.write(f"**{key} :** {value}")

# ======================================
# SIDEBAR MENU (équivalent CLI)
# ======================================

st.sidebar.markdown("---")

pages = {
    "🏠 Accueil": "Accueil",
    "🔎 Recherche titre": "Recherche par titre",
    "🎯 Recherche avancée": "Recherche avancée",
    "📖 Synopsis": "Synopsis",
    "🧠 Recherche floue": "Recherche floue",
    "⚡ Auto-complétion": "Auto-complétion",
    "📊 Stats globales": "Statistiques globales",
    "📂 Analyses": "Analyses catégories",
    "📈 Analytics avancées": "Analyses avancées"
}

if "menu" not in st.session_state:
    st.session_state.menu = "Accueil"

for label, page in pages.items():

    if st.sidebar.button(label, use_container_width=True):

        st.session_state.menu = page


menu = st.session_state.menu

if menu == "Accueil":

    st.markdown("""
    ### Bienvenue 👋
    Explore ton moteur de recherche de films basé sur Elasticsearch.
    """)

    st.divider()

    st.subheader("🚀 Accès rapide aux fonctionnalités")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🔎 Recherche par titre"):
            st.session_state.menu = "Recherche par titre"

        if st.button("🎯 Recherche avancée"):
            st.session_state.menu = "Recherche avancée"

        if st.button("📖 Synopsis"):
            st.session_state.menu = "Synopsis"

        if st.button("🧠 Recherche floue"):
            st.session_state.menu = "Recherche floue"

    with col2:

        if st.button("⚡ Auto-complétion"):
            st.session_state.menu = "Auto-complétion"

        if st.button("📊 Statistiques globales"):
            st.session_state.menu = "Statistiques globales"

        if st.button("📂 Analyses catégories"):
            st.session_state.menu = "Analyses catégories"

        if st.button("📈 Analyses avancées"):
            st.session_state.menu = "Analyses avancées"

    st.divider()

    st.info("💡 Utilise les boutons ou le menu latéral pour naviguer.")


# ======================================
# SEARCH TITLE
# ======================================

elif menu == "Recherche par titre":

    st.header("🔎 Recherche par titre")

    titre = st.text_input("Titre du film")

    if st.button("Rechercher"):
        results = search_by_title(es, titre)
        display_results(results)


# ======================================
# ADVANCED SEARCH
# ======================================

elif menu == "Recherche avancée":

    st.header("🎯 Recherche avancée")

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Titre")
        actor = st.text_input("Acteur")
        director = st.text_input("Réalisateur")
        genre = st.text_input("Genre")

    with col2:
        min_rating = st.number_input("Note min",min_value=0,max_value=10,value=0,step=1)
        max_rating = st.number_input("Note max",min_value=0,max_value=10,value=10,step=1)
        year_from = st.number_input("Année min", 1900, 2100, 1900)
        year_to = st.number_input("Année max", 1900, 2100, 2100)

    if st.button("Lancer"):
        results = search_advanced(
            es,
            title=title or None,
            actor=actor or None,
            director=director or None,
            genre=genre or None,
            min_rating=min_rating,
            max_rating=max_rating,
            year_from=year_from,
            year_to=year_to
        )
        display_results(results)


# ======================================
# SYNOPSIS
# ======================================

elif menu == "Synopsis":

    st.header("📖 Recherche dans le synopsis")

    keywords = st.text_area("Mots-clés")

    if st.button("Rechercher"):
        results = search_plot(es, keywords)
        display_results(results)


# ======================================
# FUZZY SEARCH
# ======================================

elif menu == "Recherche floue":

    st.header("🧠 Recherche floue")

    term = st.text_input("Terme")

    if st.button("Rechercher"):
        results = search_fuzzy(es, term)
        display_results(results)


# ======================================
# AUTOCOMPLETE
# ======================================

elif menu == "Auto-complétion":

    st.header("⚡ Auto-complétion")

    prefix = st.text_input("Début du titre")

    if st.button("Rechercher") :
        results = suggest_titles(es, prefix)
        display_results(results)


# ======================================
# GLOBAL STATS
# ======================================

elif menu == "Statistiques globales":

    st.header("📊 Statistiques globales")

    results = global_stats(es)

    if results:

        summary_list, best_list, worst_list = results
        summary, best, worst = summary_list[0], best_list[0], worst_list[0]

        # =========================
        # 📊 KPI CARDS
        # =========================

        st.subheader("📌 Indicateurs clés")

        col1, col2 = st.columns(2)

        col1.metric(
            "🎬 Nombre de films",
            summary.get("nombre_total_films", "N/A")
        )

        col2.metric(
            "⭐ Note moyenne",
            round(summary.get("moyenne_notes", 0), 2)
        )

        st.divider()

        # =========================
        # 🏆 BEST / WORST
        # =========================

        colA, colB = st.columns(2)

        with colA:

            st.subheader("🏆 Meilleur film")

            if isinstance(best, dict):
                st.markdown(f"""
                **🎬 {best.get('titre', 'N/A')}**  
                ⭐ Note : {best.get('note', 'N/A')}  
                """)
            else:
                st.write(best)

        with colB:

            st.subheader("💀 Pire film")

            if isinstance(worst, dict):
                st.markdown(f"""
                **🎬 {worst.get('titre', 'N/A')}**  
                ⭐ Note : {worst.get('note', 'N/A')}  
                """)
            else:
                st.write(worst)


# ======================================
# ANALYSES CATÉGORIES
# ======================================

elif menu == "Analyses catégories":

    st.header("📂 Analyses par catégories")

    tabs = st.tabs(
        [
            "Top genres",
            "Top acteurs",
            "Top réalisateurs",
            "Distribution années"
        ]
    )

    with tabs[0] :
        st.dataframe(top_genres(es))

    with tabs[1] :
        st.dataframe(top_actors(es))

    with tabs[2] :
        st.dataframe(top_directors(es))

    with tabs[3] :
        st.dataframe(distribution(es))


# ======================================
# ANALYSES AVANCÉES
# ======================================

elif menu == "Analyses avancées":

    st.header("📈 Analyses avancées")

    
    tabs = st.tabs([
        "Evolution note",
            "Genres mieux notés",
            "Réalisateurs mieux notés"
    ])

    with tabs[0] :
            data = evolution_note(es)
            st.plotly_chart(
            {
                "data": [
                    {
                        "x": [d["annee"] for d in data],
                        "y": [d["note_moyenne"] for d in data],
                        "type": "scatter",
                        "mode": "lines+markers",
                        "hovertemplate":
                            "Année: %{x}<br>"
                            "Note moyenne: %{y:.2f}<br>"
                            "Nombre de films: %{customdata}<extra></extra>",
                        "customdata": [d["nb_films"] for d in data],
                    }
                ],
                "layout": {
                    "title": "Évolution de la note moyenne",
                    "xaxis": {"title": "Année"},
                    "yaxis": {"title": "Note moyenne"},
                }
            }
        )

    with tabs[1] :
        st.dataframe(best_rated_genres(es))

    with tabs[2] :
        st.dataframe(best_rated_directors(es))