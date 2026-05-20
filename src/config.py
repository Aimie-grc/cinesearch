from elasticsearch import Elasticsearch


def create_mapping(es):

    mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "standard"
            },
            "directors": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "actors": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "genres": {
                "type": "keyword"
            },
            "year": {
                "type": "integer"
            },
            "rating": {
                "type": "float"
            },
            "rank": {
                "type": "integer"
            },
            "release_date": {
                "type": "date"
            },
            "plot": {
                "type": "text",
                "analyzer": "standard"
            },
            "running_time_secs": {
                "type": "integer"
            },
            "image_url": {
                "type": "keyword"
            }
        }
    }
    if es.indices.exists(index="movies"):
        es.indices.delete(index="movies")
    else :
        es.indices.create(index="movies", mappings=mappings)
    return es

