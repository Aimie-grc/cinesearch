from elasticsearch import Elasticsearch
from src.analytics import top_genres

es = Elasticsearch("http://localhost:9200")


def test_top_genres_not_empty():
    results = top_genres(es)

    assert len(results) > 0
