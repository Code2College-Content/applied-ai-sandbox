"""Tests for M7 search feature."""
import pytest
from app import create_app


@pytest.fixture
def app():
    a = create_app()
    a.config["TESTING"] = True
    return a


@pytest.fixture
def client(app):
    return app.test_client()


def seed(app, notes):
    app.notes.clear()
    app.notes.extend(notes)


def test_search_returns_matching_notes(client, app):
    seed(app, [
        {"title": "Flask tutorial", "body": "Learn Flask routes", "tags": []},
        {"title": "Python basics", "body": "Variables and loops", "tags": []},
    ])
    r = client.get("/search?q=flask")
    assert b"Flask tutorial" in r.data
    assert b"Python basics" not in r.data


def test_search_case_insensitive(client, app):
    seed(app, [{"title": "Flask Guide", "body": "About Flask", "tags": []}])
    r = client.get("/search?q=FLASK")
    assert b"Flask Guide" in r.data


def test_empty_query_redirects_home(client):
    r = client.get("/search?q=")
    assert r.status_code in (301, 302, 303)


def test_whitespace_query_redirects_home(client):
    r = client.get("/search?q=   ")
    assert r.status_code in (301, 302, 303)


def test_search_no_results_shows_empty_state(client, app):
    seed(app, [{"title": "Hello", "body": "World", "tags": []}])
    r = client.get("/search?q=zzznomatch")
    assert b"No notes match" in r.data


def test_search_none_fields_dont_crash(client, app):
    seed(app, [{"title": None, "body": None, "tags": []}])
    r = client.get("/search?q=test")
    assert r.status_code == 200


def test_search_highlights_match(client, app):
    seed(app, [{"title": "Flask note", "body": "Flask is great", "tags": []}])
    r = client.get("/search?q=flask")
    assert b"<mark>" in r.data


def test_search_matches_body(client, app):
    seed(app, [{"title": "Unrelated title", "body": "Flask is mentioned here", "tags": []}])
    r = client.get("/search?q=flask")
    assert b"Unrelated title" in r.data
