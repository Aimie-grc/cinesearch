def global_stats(es, index="movies"):
    """Calcule les statistiques globales du dataset."""
    aggs = {"avg_rating" :{"avg": {"field": "rating"}},
            "min_rating" :{"min": {"field": "rating"}},
            "max_rating" :{"max": {"field": "rating"}}}
    result = es.search(index=index, size=0, aggs=aggs)
    aggregations = result['aggregations']
    
    print("Nombre total de films :", result["hits"]["total"]["value"])
    print(f"Moyenne des notes : {aggregations['avg_rating']['value']:.2f}")
    print(f"Note minimale : {aggregations['min_rating']['value']:.2f}")
    print(f"Note maximale : {aggregations['max_rating']['value']:.2f}")

def top_genres(es, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {
    # TODO: Définissez une terms aggregation sur le champ "genres"
    # Indice: {"genres": {"terms": {"field": "genres", "size": size}}}
    }
    result = es.search(index=index, size=0, aggs=aggs)
    # TODO: Parcourez result["aggregations"]["genres"]["buckets"]
    # Chaque bucket contient "key" (le genre) et "doc_count" (nombre de films)
    pass

def best_rated_directors(es, min_films=3, index="movies"):
    """Réalisateurs avec la meilleure note moyenne (min N films)."""
    aggs = {
    # TODO: Construisez une agrégation imbriquée :
    # 1. terms aggregation sur "directors.keyword"
    # 2. Sub-aggregation avg sur "rating"
    # 3. bucket_selector pour filtrer min_films
    # Indice: {"directors": {"terms": {...}, "aggs": {...}}}
    }
    result = es.search(index=index, size=0, aggs=aggs)
    # TODO: Trier les buckets par note moyenne décroissante
    # et afficher le top 10
    # Indice: sorted(buckets, key=lambda x: x["avg_rating"]["value"], reverse=True)
    pass