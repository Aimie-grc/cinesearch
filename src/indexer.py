from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

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


es.indices.create(index="movies", mappings=mappings)

