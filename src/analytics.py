def global_stats(es, index="movies"):
    """Calcule les statistiques globales du dataset."""
    aggs = {"avg_rating" :{"avg": {"field": "rating"}},
            "min_rating" :{"min": {"field": "rating"}},
            "max_rating" :{"max": {"field": "rating"}}}
    result = es.search(index=index, size=0, aggs=aggs)
    aggregations = result['aggregations']
    
    sortie = [{"Nombre total de films": result["hits"]["total"]["value"],
    "Moyenne des notes" : round(aggregations['avg_rating']['value'],2),
    "Note minimale" : round(aggregations['min_rating']['value'],2),
    "Note maximale" : round(aggregations['max_rating']['value'],2)}] # Liste pour faciliter l'affichage

    return sortie

def top_genres(es, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {"Top genres": {"terms": {"field": "genres", "size": size}}}
    result = es.search(index=index, size=0, aggs=aggs)

    return [
        {"genre" : bucket["key"],
         "nb_films " : bucket["doc_count"]}
        for bucket in result["aggregations"]["Top genres"]["buckets"]
    ]


def top_directors(es, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {"Top réalisateurs" : {"terms": {"field": "directors.keyword", "size": size}}}
    result = es.search(index=index, size=0, aggs=aggs)

    return [
        {"realisateur" : bucket["key"],
         "nb_films " : bucket["doc_count"]}
        for bucket in result["aggregations"]["Top réalisateurs"]["buckets"]
    ]

def top_actors(es, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {"Top acteurs" : {"terms": {"field": "actors.keyword", "size": size}}}
    result = es.search(index=index, size=0, aggs=aggs)

    return [
        {"acteur" : bucket["key"],
         "nb_films " : bucket["doc_count"]}
        for bucket in result["aggregations"]["Top acteurs"]["buckets"]
    ]

def distribution(es, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {"Distribution par décennies" : {"histogram" : {"field": "year", "interval" : 10}}}
    result = es.search(index=index, size=0, aggs=aggs)

    return [
        {"decennie" : f'{int(bucket["key"])}-{int(bucket["key"])+9}',
         "nb_films " : bucket["doc_count"]}
        for bucket in result["aggregations"]["Distribution par décennies"]["buckets"]
    ]


def evolution_note(es, index="movies"):
    aggs = {"evolution_note": {
        "terms": {"field": "year", "size" : 100},
        "aggs": {"avg_rating": {"avg": {"field": "rating"}},
                "film_count" : {"value_count" : {"field" : "rating"}}
        }}}
    

    result = es.search(index=index, size=0, aggs=aggs)

    buckets = result["aggregations"]["evolution_note"]["buckets"]

    # tri par annee croissante
    sorted_buckets = sorted(
        buckets,
        key=lambda x: x["key"],
    )

    return [
        {"annee" : b["key"],
         "note_moyenne" : round(b["avg_rating"]["value"], 2) if b["avg_rating"]["value"] else None,
         "nb_films " : b["film_count"]["value"]}
        for b in sorted_buckets
    ]


def best_rated_genres(es, index="movies"):
    aggs = {"genres": {
            "terms": {"field": "genres", "size" : 100},
            "aggs": {"avg_rating": {"avg": {"field": "rating"}},
                    "film_count" : {"value_count" : {"field" : "rating"}}
            }}}
    

    result = es.search(index=index, size=0, aggs=aggs)

    buckets = result["aggregations"]["genres"]["buckets"]

    # tri par note moyenne décroissante
    sorted_buckets = sorted(
        buckets,
        key=lambda x: x["avg_rating"]["value"],
        reverse=True
    )

    return [
        {"genre" : b["key"],
         "note_moyenne" : round(b["avg_rating"]["value"],2),
         "nb_films " : b["film_count"]["value"]}
        for b in sorted_buckets[:10]
    ]


def best_rated_directors(es, min_films=3, index="movies"):
    """Réalisateurs avec la meilleure note moyenne (min N films)."""
    aggs = {"directors": {
            "terms": {"field": "directors.keyword", "size" : 100},
            "aggs": {"avg_rating": {"avg": {"field": "rating"}},
                    "film_count" : {"value_count" : {"field" : "rating"}},
                    "min_films_filter" : {"bucket_selector" :{ 
                                        "buckets_path":{"count" : "film_count"},
                                        "script" : f"params.count >= {min_films}"
                                        }}
            }}}
    

    result = es.search(index=index, size=0, aggs=aggs)

    buckets = result["aggregations"]["directors"]["buckets"]

    # tri par note moyenne décroissante
    sorted_buckets = sorted(
        buckets,
        key=lambda x: x["avg_rating"]["value"],
        reverse=True
    )

    return [
        {"directeur" : b["key"],
         "note_moyenne" : round(b["avg_rating"]["value"],2),
         "nb_films " : b["film_count"]["value"]}
        for b in sorted_buckets[:10]
    ]
