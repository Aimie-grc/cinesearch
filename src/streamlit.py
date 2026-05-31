import streamlit as st
from elasticsearch import Elasticsearch

from config import create_mapping
from indexer import index_movies
from search import search_by_title, search_advanced, search_plot,search_fuzzy, suggest_titles
from analytics import global_stats, top_genres, top_actors, top_directors, distribution, best_rated_directors, best_rated_genres, evolution_note


st.set_page_config(
    page_title="CineSearch",
    page_icon="🎬",
    layout="wide"
)

@st.cache_resource
def get_es():
    es = Elasticsearch("http://localhost:9200")
    es.info()
    return es


try:
    es = get_es()

    st.sidebar.success("Elasticsearch connecté")

    if not es.indices.exists(index="movies"):
        st.sidebar.warning("Index 'movies' introuvable")
        create_mapping(es)
        index_movies(es, "data/movies_cleaned_v2.json")

except Exception as e:
    st.error(f"Impossible de se connecter à Elasticsearch : {e}")
    st.stop()


def display_results(results):

    if not results:
        st.warning("Aucun résultat trouvé.")
        return

    for movie in results:

        with st.expander(
            f"{movie.get('title', 'Titre inconnu')} "
            f"({movie.get('year', 'N/A')})"
        ):

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Réalisateur :**", movie.get("director"))
                st.write("**Genre :**", movie.get("genre"))
                st.write("**Note :**", movie.get("rating"))

            with col2:
                st.write("**Acteurs :**")
                st.write(movie.get("actors"))

            st.write("**Synopsis :**")
            st.write(movie.get("plot"))

st.sidebar.title("🎬 CineSearch")

menu = st.sidebar.radio(
    "Choisissez une fonctionnalité",
    [
        "Recherche par titre",
        "Recherche avancée",
        "Recherche synopsis",
        "Recherche floue",
        "Auto-complétion",
        "Statistiques globales",
        "Analyses par catégorie",
        "Analyses avancées"
    ]
)

st.title("🎥 CineSearch")

if menu == "Recherche par titre":

    st.header("Recherche par titre")

    titre = st.text_input("Titre du film")

    if st.button("Rechercher"):

        results = search_by_title(es, titre)

        display_results(results)

elif menu == "Recherche avancée":

    st.header("Recherche avancée")

    col1, col2 = st.columns(2)

    with col1:

        title = st.text_input("Titre")

        actor = st.text_input("Acteur")

        director = st.text_input("Réalisateur")

        genre = st.text_input("Genre")

    with col2:

        min_rating = st.number_input(
            "Note minimum",
            min_value=0.0,
            max_value=10.0,
            value=0.0
        )

        max_rating = st.number_input(
            "Note maximum",
            min_value=0.0,
            max_value=10.0,
            value=10.0
        )

        year_from = st.number_input(
            "Année minimum",
            min_value=1900,
            max_value=2100,
            value=1900
        )

        year_to = st.number_input(
            "Année maximum",
            min_value=1900,
            max_value=2100,
            value=2100
        )

    if st.button("Lancer la recherche avancée"):

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


elif menu == "Recherche synopsis":

    st.header("Recherche dans le synopsis")

    keywords = st.text_area(
        "Mots-clés à rechercher"
    )

    if st.button("Rechercher"):

        results = search_plot(es, keywords)

        display_results(results)

elif menu == "Recherche floue":

    st.header("Recherche floue")

    term = st.text_input(
        "Terme recherché"
    )

    if st.button("Rechercher"):

        results = search_fuzzy(es, term)

        display_results(results)

elif menu == "Auto-complétion":

    st.header("Auto-complétion")

    prefix = st.text_input(
        "Début du titre"
    )

    if prefix:

        suggestions = suggest_titles(es, prefix)

        st.subheader("Suggestions")

        for suggestion in suggestions:
            st.write("•", suggestion)

elif menu == "Statistiques globales":

    st.header("Statistiques globales")

    stats = global_stats(es)
    display_results(stats)

    # col1, col2, col3 = st.columns(3)

    # col1.metric(
    #     "Nombre de films",
    #     stats["total_movies"]
    # )

    # col2.metric(
    #     "Note moyenne",
    #     round(stats["avg_rating"], 2)
    # )

    # col3.metric(
    #     "Nombre de genres",
    #     stats["genres_count"]
    # )

elif menu == "Analyses par catégorie":

    st.header("Top réalisateurs / acteurs / genres et distribution des films par décennie")

    tabs = st.tabs([
        "Top genres",
        "Top réalisateurs",
        "Top acteurs",
        "Films par décennie"
    ])

    with tabs[0]:

        genres = top_genres(es)

        st.bar_chart(genres)

    with tabs[1]:

        directors = top_directors(es)

        st.bar_chart(directors)

    with tabs[2]:

        actors = top_actors(es)

        st.bar_chart(actors)
    
    with tabs[3]:
        pass

elif menu == "Analyses avancées":

    st.header("Évolution de la note moyenne par année, Genre le mieux noté en moyenne et Réalisateur avec la meilleure note moyenne")

    tabs = st.tabs([
        "Évolution note moyenne",
        "Genre le mieux noté",
        "Meileur réalisateur"
    ])

    with tabs[0]:

        genres = top_genres(es)

        st.bar_chart(genres)

    with tabs[1]:

        directors = top_directors(es)

        st.bar_chart(directors)

    with tabs[2]:

        actors = top_actors(es)

        st.bar_chart(actors)