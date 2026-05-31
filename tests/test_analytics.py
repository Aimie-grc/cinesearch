from elasticsearch import Elasticsearch
from src.analytics import global_stats, top_genres, top_actors, top_directors, distribution, best_rated_directors, best_rated_genres, evolution_note

es = Elasticsearch("http://localhost:9200")


def test_global_stats_nb_ok():
    results = global_stats(es)

    assert results[0]['Nombre total de films'] == es.count(index="movies")["count"]

def test_global_stats_note_moy_ok():
    results = global_stats(es)

    assert results[0]['Moyenne des notes'] >= 0
    assert results[0]['Moyenne des notes'] <= 10

def test_top_genres_not_empty():
    results = top_genres(es)

    assert len(results) > 0

def test_top_actors_not_empty():
    results = top_actors(es)

    assert len(results) > 0

def test_top_directors_not_empty():
    results = top_directors(es)

    assert len(results) > 0

def test_distribution_not_empty():
    results = distribution(es)

    assert len(results) > 0


def test_distribution_contains_decennie():
    results = distribution(es)

    assert "decennie" in results[0]
    assert "nb_films " in results[0]


def test_top_genres_note_decroissante():
    results = best_rated_genres(es)

    notes = [r["note_moyenne"] for r in results]

    assert notes == sorted(notes, reverse=True)


def test_evolution_note_annee_croissante():
    results = evolution_note(es)

    annees = [r["annee"] for r in results]

    assert annees == sorted(annees)


def test_evolution_note_contains_fields():
    results = evolution_note(es)

    assert "annee" in results[0]
    assert "note_moyenne" in results[0]
    assert "nb_films " in results[0]


def test_best_rated_directors_film_min():
    results = best_rated_directors(es)

    assert all(r["nb_films "] >= 3 for r in results)


def test_best_rated_directors_note_decroissante():
    results = best_rated_directors(es)

    notes = [r["note_moyenne"] for r in results]

    assert notes == sorted(notes, reverse=True)