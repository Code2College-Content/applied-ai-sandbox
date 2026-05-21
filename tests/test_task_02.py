"""Acceptance tests for TASK 02 — delete a note."""

from werkzeug.security import generate_password_hash

from models import create_user


def _seed(app, owner="1", n=2):
    app.notes.clear()
    for i in range(n):
        app.notes.append(
            {"title": f"Note {i}", "body": f"Body {i}", "owner": owner}
        )


def test_anonymous_home_redirects_to_login(client):
    r = client.get("/")
    assert r.status_code in (302, 303)
    assert "/login" in r.headers["Location"]


def test_delete_removes_note(client, app, auth):
    auth.login()
    _seed(app, owner="1", n=2)
    r = client.post("/notes/0/delete")
    assert r.status_code in (302, 303)
    assert len(app.notes) == 1
    assert app.notes[0]["title"] == "Note 1"


def test_delete_get_returns_405(client, app, auth):
    auth.login()
    _seed(app, owner="1", n=1)
    r = client.get("/notes/0/delete")
    assert r.status_code == 405


def test_delete_nonexistent_returns_404(client, app, auth):
    auth.login()
    _seed(app, owner="1", n=1)
    r = client.post("/notes/99/delete")
    assert r.status_code == 404


def test_homepage_has_delete_form(client, app, auth):
    auth.login()
    _seed(app, owner="1", n=1)
    r = client.get("/")
    body = r.data.decode()
    assert "/notes/0/delete" in body


def test_users_see_only_their_own_notes(client, app):
    with app.app_context():
        create_user("other", generate_password_hash("secret2"))

    client.post("/login", data={"username": "testuser", "password": "secret"})
    app.notes.clear()
    app.notes.append({"title": "Mine", "body": "A", "owner": "1"})
    app.notes.append({"title": "Other", "body": "B", "owner": "2"})

    r = client.get("/")
    assert b"Mine" in r.data
    assert b"Other" not in r.data

    client.get("/logout")
    client.post("/login", data={"username": "other", "password": "secret2"})

    r = client.get("/")
    assert b"Other" in r.data
    assert b"Mine" not in r.data
