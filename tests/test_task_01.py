"""Acceptance tests for TASK 01 — validate the new-note form.

Don't edit these to make them pass. Change app.py / templates instead.
"""


def test_empty_title_shows_error(client):
    r = client.post("/notes/new", data={"title": "", "body": "hi"})
    assert r.status_code == 200
    assert b"Title is required" in r.data


def test_empty_body_shows_error(client):
    r = client.post("/notes/new", data={"title": "Hello", "body": ""})
    assert r.status_code == 200
    assert b"Body is required" in r.data


def test_valid_submit_redirects_and_persists(client, app):
    app.notes.clear()
    r = client.post(
        "/notes/new", data={"title": "First", "body": "Hello world", "tags": "python, flask"},
    )
    assert r.status_code in (302, 303)
    assert any(n["title"] == "First" for n in app.notes)
    assert app.notes[0]["tags"] == ["python", "flask"]


def test_invalid_submit_preserves_typed_values(client):
    r = client.post("/notes/new", data={"title": "Half typed", "body": ""})
    assert r.status_code == 200
    # User's typed-in title should still be in the rendered form
    assert b"Half typed" in r.data
