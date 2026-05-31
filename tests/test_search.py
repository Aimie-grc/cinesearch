from elasticsearch import Elasticsearch
from src.search import search_by_title, search_advanced, suggest_titles, search_fuzzy, search_plot

es = Elasticsearch("http://localhost:9200")


def test_search_by_title_returns_results():
    results = search_by_title(es, "Batman")

    assert len(results) > 0

def test_search_by_title_has_title():
    results = search_by_title(es, "Batman")

    first = results[0]

    assert "title" in first

def test_search_unknown_movie():
    results = search_by_title(es, "azertyuiopqsdfgh")

    assert results == []



def test_search_advanced_returns_results():
    results = search_advanced(
        es,
        title="Batman"
    )

    assert len(results) > 0

def test_advanced_search_rating():
    results = search_advanced(
        es,
        min_rating=9
    )

    assert all(r["rating"] >= 9 for r in results)

def test_suggest_titles_returns_results():
    results = suggest_titles(
        es,
        "Bat"
    )

    assert len(results) > 0


def test_suggest_titles_contains_prefix():
    results = suggest_titles(
        es,
        "Incep"
    )

    titles = [r["title"] for r in results]

    assert any("Incep" in title for title in titles)


def test_search_fuzzy_typo():
    results = search_fuzzy(
        es,
        "Batmn"
    )

    assert len(results) > 0

def test_search_plot_returns_results():
    results = search_plot(
        es,
        "dream"
    )

    assert len(results) > 0


def test_search_plot_contains_highlight():
    results = search_plot(
        es,
        "dream"
    )

    assert any("highlights" in r for r in results)