import time
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# Attendre qu'Elasticsearch soit prêt
for i in range(30):
    try:
        es.info()
        print("Elasticsearch est prêt !")
        break
    except Exception:
        print(f"En attente d'Elasticsearch... ({i+1}/30)")
        time.sleep(2)