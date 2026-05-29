"""Tests for M7 – Starred Notes feature."""
import pytest
from app import create_app


@pytest.fixture
def auth_client():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    app.users["tester"] = "pw"
    with client.session_transaction() as sess:
        sess["username"] = "tester"
    return client, app


def test_new_note_starred_defaults_false(auth_client):
    client, app = auth_client
    client.post("/notes/new", data={"title": "Hello", "body": "World"})
    assert app.notes[0]["starred"] is False


def test_star_note_toggles_to_true(auth_client):
    client, app = auth_client
    client.post("/notes/new", data={"title": "Hello", "body": "World"})
    client.post("/notes/0/star")
    assert app.notes[0]["starred"] is True


def test_star_note_toggles_back_to_false(auth_client):
    client, app = auth_client
    client.post("/notes/new", data={"title": "Hello", "body": "World"})
    client.post("/notes/0/star")
    client.post("/notes/0/star")
    assert app.notes[0]["starred"] is False


def test_star_note_out_of_range_returns_404(auth_client):
    client, _ = auth_client
    resp = client.post("/notes/99/star")
    assert resp.status_code == 404


def test_star_icon_shown_in_home(auth_client):
    client, _ = auth_client
    client.post("/notes/new", data={"title": "A", "body": "B"})
    resp = client.get("/")
    assert b"&#9734;" in resp.data or b"star" in resp.data


def test_starred_note_has_class_in_home(auth_client):
    client, _ = auth_client
    client.post("/notes/new", data={"title": "A", "body": "B"})
    client.post("/notes/0/star")
    resp = client.get("/")
    assert b'class="note starred"' in resp.data
