from tqdm import tqdm
import time
import json
from elasticsearch.helpers import bulk

def index_movies(es, filename, index_name="movies"):
    start = time.time()
    actions = []
    
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i in tqdm(range(1, len(lines), 2), desc="Préparation des documents"):
        doc = json.loads(lines[i].strip())
        movie = doc["fields"]
        actions.append({
            "_index": index_name,
            "_source": movie
        })
    
    try:
        success, errors = bulk(es, actions, raise_on_error=False)
        es.indices.refresh(index=index_name)

        print(f"{success} films indexés avec succès")

        if errors:
            print(f"{len(errors)} erreurs rencontrées")

    except Exception as e:
        print(f"Erreur lors de l'indexation : {e}")
    
    elapsed = time.time() - start
    print(f"Temps total: {elapsed:.2f}s")

    return es

def verif_es(es):
    # Vérifier le nombre de documents
    count = es.count(index="movies")["count"]
    print(f"Nombre de documents indexés: {count}")

    # Afficher un échantillon
    result = es.search(index="movies", size=3)
    print("Échantillon de documents :")
    for hit in result["hits"]["hits"]:
        print(hit["_source"]["title"], "-", hit["_source"]["rating"])

    # Vérifier le mapping
    mapping = es.indices.get_mapping(index="movies")
    print("Mapping de l'index movies :")
    print(json.dumps(mapping.body, indent=2))