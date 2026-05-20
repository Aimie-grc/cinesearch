import time
from elasticsearch import Elasticsearch

from config import create_mapping
from indexer import index_movies, verif_es
from search import search_by_title, search_advanced, search_plot,search_fuzzy, suggest_titles

es = Elasticsearch("http://localhost:9200")

# Attendre qu'Elasticsearch soit prêt
# for i in range(30):
#     try:
#         es.info()
#         print("Elasticsearch est prêt !")
#         break
#     except Exception:
#         print(f"En attente d'Elasticsearch... ({i+1}/30)")
#         time.sleep(2)

es = create_mapping(es)
es = index_movies(es,'data/movies_cleaned_v2.json')
# verif_es(es)
print('\n')
print('Search by title "Don Jon"')
search_by_title(es, 'Don Jon')
print('Search advanced')
search_advanced(
    es,
    title="Batman",
    genre="Action",
    min_rating=7,
    year_from=2005
)
