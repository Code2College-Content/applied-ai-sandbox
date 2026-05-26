"""Tests for M7 — full-text search on GET /?q="""
import pytest


@pytest.fixture(autouse=True)
def seed_notes(app, client):
    app.notes.clear()
    client.post("/notes/new", data={"title": "Flask basics", "body": "Routing and views in Flask."})
    client.post("/notes/new", data={"title": "Python tips", "body": "List comprehensions are fast."})
    client.post("/notes/new", data={"title": "Database design", "body": "Indexes improve query speed."})


def test_search_returns_matching_notes(client):
    r = client.get("/?q=Flask")
    assert r.status_code == 200
    assert b"Flask basics" in r.data
    assert b"Python tips" not in r.data


def test_search_excludes_nonmatching(client):
    r = client.get("/?q=nonexistentterm")
    assert r.status_code == 200
    assert b"Flask basics" not in r.data
    assert b"Python tips" not in r.data


def test_search_case_insensitive(client):
    r = client.get("/?q=flask")
    assert r.status_code == 200
    assert b"Flask basics" in r.data


def test_search_body_match(client):
    r = client.get("/?q=comprehensions")
    assert r.status_code == 200
    assert b"Python tips" in r.data
    assert b"Flask basics" not in r.data


def test_search_snippet_contains_mark(client):
    r = client.get("/?q=Routing")
    assert r.status_code == 200
    assert b"<mark>" in r.data


def test_search_empty_query_returns_all(client):
    r = client.get("/?q=")
    assert r.status_code == 200
    assert b"Flask basics" in r.data
    assert b"Python tips" in r.data
    assert b"Database design" in r.data


def test_no_query_returns_all(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Flask basics" in r.data
    assert b"Python tips" in r.data


def test_search_no_results_shows_message(client):
    r = client.get("/?q=zzznomatch")
    assert r.status_code == 200
    assert b"No notes match" in r.data


def test_title_match_outranks_body_match(client, app):
    # "Flask" appears in title of note 1 and body of note 2 doesn't have it —
    # more directly: add a note where query is only in body, check title-match comes first.
    app.notes.clear()
    client.post("/notes/new", data={"title": "speed tricks", "body": "Indexes improve query speed."})
    client.post("/notes/new", data={"title": "Indexes explained", "body": "A brief intro."})
    r = client.get("/?q=Indexes")
    assert r.status_code == 200
    data = r.data.decode()
    # Title match ("Indexes explained") should appear before body match ("speed tricks")
    assert data.index("Indexes explained") < data.index("speed tricks")


def test_search_highlight_in_title(client):
    r = client.get("/?q=Python")
    assert r.status_code == 200
    assert b"<mark>Python</mark>" in r.data or b"<mark>python</mark>" in r.data.lower()
