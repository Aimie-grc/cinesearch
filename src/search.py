from elasticsearch import Elasticsearch as es

def search_by_title(es, title, index="movies"):
    """Recherche des films par titre (match query)."""
    query = {"match" : {"title" : title }}
    results = es.search(index=index, query=query, size=10)
    
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
        print("Année :", source.get("year", "N/A"))
        print("Note :", source.get("rating", "N/A"))
        print("Réalisateur(s) :", source.get("directors", "N/A"))
        print("Score de pertinence :", hit["_score"])
        print("\n")
    
    if not hits :
        print("Aucun film trouvé.")
    

def search_advanced(es, title=None, actor=None, director=None,
genre=None, min_rating=None, max_rating=None,
year_from=None, year_to=None, index="movies"):
    must = []
    filters = []
    if title:
        must.append({"match": {"title": title}})
    if actor:
        must.append({"match": {"actors": actor}})
    if director:
        must.append({"match": {"directors": director}})
    if genre:
        filters.append({"match": {"genres": genre}})
    
    rating_range = {}
    if min_rating is not None:
        rating_range["gte"] = min_rating
    if max_rating is not None:
        rating_range["lte"] = max_rating
    if rating_range:
        filters.append({"range": {"rating": rating_range}})
    
    year_range = {}
    if year_from is not None:
        year_range["gte"] = year_from
    if year_to is not None:
        year_range["lte"] = year_to
    if year_range:
        filters.append({"range": {"year": year_range}})

    query = {"bool": {"must": must, "filter": filters}}
    results = es.search(index=index, query=query, size=10)
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
        print("Acteur(s) :", source.get("actors", "N/A"))
        print("Genre(s) :", source.get("genres", "N/A"))
        print("Année :", source.get("year", "N/A"))
        print("Note :", source.get("rating", "N/A"))
        print("Réalisateur(s) :", source.get("directors", "N/A"))
        print("Score de pertinence :", hit["_score"])
        print("\n")
    
    if not hits :
        print("Aucun film trouvé.")

def search_plot(es, keywords, index="movies"):
    """Recherche dans le synopsis avec mise en évidence des termes."""
    query = {"match" : {"plot" : keywords }}
    highlight = {"fields": {"plot": {"fragment_size": 150, "number_of_fragments" : 3}}}
    results = es.search(index=index, query=query, highlight=highlight)
    
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
        
        if "highlight" in hit :
            for fragment in enumerate(hit['highlight']['plot'], start = 1):
                i, f = fragment
                print(f"Fragment {i}:", f)
                print("\n")
    
    if not hits :
        print("Aucun film trouvé.")

def search_fuzzy(es, title, fuzziness=2, index="movies"):
    """Recherche tolérante aux fautes de frappe."""
    query = {"match": {"title": {"query": title, "fuzziness": fuzziness}}}
    results = es.search(index=index, query=query)
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
        print("Score de pertinence :", hit["_score"])
        print("\n")
    
    if not hits :
        print("Aucun film trouvé.")

# Option 1 : Prefix query (plus simple)
def suggest_titles(es, prefix, index="movies"):
    """Auto-complétion basée sur un préfixe."""
    query = {"prefix": {"title": prefix.lower()}}
    
    results = es.search(index=index, query=query)
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
    
    if not hits :
        print("Aucune suggestion possible.")

# Option 2 : Completion suggester (plus performant)
# Nécessite un champ "suggest" de type "completion" dans le mapping
def suggest_titles_2(es, prefix, index="movies"):
    """Auto-complétion basée sur un préfixe."""
    query = {"prefix": {"title": prefix.lower()}}
    
    results = es.search(index=index, query=query)
    hits = results['hits']['hits']
    for hit in hits :
        source = hit["_source"]
        print("Titre :", source.get("title", "N/A"))
    
    if not hits :
        print("Aucune suggestion possible.")