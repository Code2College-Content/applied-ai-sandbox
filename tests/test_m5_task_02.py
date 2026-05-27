"""Acceptance tests for M5 Task 2 — star/unstar notes and filter by starred."""


def _seed(app, n=2):
    app.notes.clear()
    for i in range(n):
        app.notes.append({"title": f"Note {i}", "body": f"Body {i}", "tags": [], "starred": False})


def test_new_note_has_starred_false(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": ""})
    assert app.notes[-1]["starred"] is False


def test_star_toggles_to_true(client, app):
    _seed(app, 1)
    r = client.post("/notes/0/star")
    assert r.status_code in (302, 303)
    assert app.notes[0]["starred"] is True


def test_star_toggles_back_to_false(client, app):
    _seed(app, 1)
    client.post("/notes/0/star")
    client.post("/notes/0/star")
    assert app.notes[0]["starred"] is False


def test_star_get_returns_405(client, app):
    _seed(app, 1)
    r = client.get("/notes/0/star")
    assert r.status_code == 405


def test_star_nonexistent_returns_404(client, app):
    _seed(app, 1)
    r = client.post("/notes/99/star")
    assert r.status_code == 404


def test_homepage_has_star_form(client, app):
    _seed(app, 1)
    r = client.get("/")
    body = r.data.decode()
    assert "/notes/0/star" in body


def test_filter_shows_starred_only(client, app):
    _seed(app, 2)
    client.post("/notes/0/star")
    r = client.get("/?starred=1")
    body = r.data.decode()
    assert "Note 0" in body
    assert "Note 1" not in body


def test_filter_empty_shows_message(client, app):
    _seed(app, 1)
    r = client.get("/?starred=1")
    body = r.data.decode()
    assert "No starred notes yet" in body
