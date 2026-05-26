"""Acceptance tests for the starred-notes feature."""


def _seed(app):
    app.notes.clear()
    app.notes.append({"title": "Unstarred", "body": "B", "tags": []})
    app.notes.append({"title": "Starred",   "body": "B", "tags": [], "starred": True})


def test_new_note_has_starred_false(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B"})
    assert app.notes[0]["starred"] is False


def test_star_toggles_to_true(client, app):
    app.notes.clear()
    app.notes.append({"title": "T", "body": "B", "starred": False})
    r = client.patch("/notes/0/star")
    assert r.status_code == 200
    assert app.notes[0]["starred"] is True


def test_star_toggles_back_to_false(client, app):
    app.notes.clear()
    app.notes.append({"title": "T", "body": "B", "starred": True})
    r = client.patch("/notes/0/star")
    assert r.status_code == 200
    assert app.notes[0]["starred"] is False


def test_star_nonexistent_returns_404(client, app):
    app.notes.clear()
    r = client.patch("/notes/99/star")
    assert r.status_code == 404


def test_starred_notes_sorted_first_in_home(client, app):
    _seed(app)
    r = client.get("/")
    body = r.data.decode()
    assert body.index("Starred") < body.index("Unstarred")


def test_home_renders_star_button(client, app):
    _seed(app)
    r = client.get("/")
    assert b"star-btn" in r.data
