def create_mapping(es):

    mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
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
                "analyzer": "standard",
                "fielddata": True
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

    es.indices.create(index="movies", mappings=mappings)
    return es

