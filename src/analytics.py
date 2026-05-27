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

def top(es, objectif, index="movies", size=10):
    """Top des genres les plus représentés."""
    aggs = {"Top genres": {"terms": {"field": "genres", "size": size}},
            "Top réalisateurs" : {"terms": {"field": "directors.keyword", "size": size}},
            "Top acteurs" : {"terms": {"field": "actors.keyword", "size": size}},
            "Distribution par décennies" : {"histogram" : {"field": "year", "interval" : 10}}
            }
    result = es.search(index=index, size=0, aggs=aggs)

    for categorie in result["aggregations"]:
        print(f"\n{categorie}")
        for bucket in result["aggregations"][categorie]["buckets"]:
            cat = bucket["key"]
            if isinstance(cat, float): # Pour les années
                cat = int(cat)
            nb_films = bucket["doc_count"]
            if categorie == "Distribution par décennies":
                print(f"{cat}-{cat+9}: {nb_films}")
            else:
                print(f"{cat}: {nb_films}")

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

    # affichage top 10
    print("\n🎬 Top réalisateurs (note moyenne) :\n")

    for b in sorted_buckets[:10]:
        director = b["key"]
        avg = b["avg_rating"]["value"]
        count = b["film_count"]["value"]

        print(f"{director} — {avg:.2f} ({count} films)")
    pass


def best_rated_genre():
    pass

def evolution_note():
    pass