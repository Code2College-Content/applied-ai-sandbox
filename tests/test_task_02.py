"""Acceptance tests for TASK 02 — delete a note."""


def _seed(app, n=2):
    app.notes.clear()
    for i in range(n):
        app.notes.append({"title": f"Note {i}", "body": f"Body {i}", "tags": []})


def test_delete_removes_note(client, app):
    _seed(app, 2)
    r = client.post("/notes/0/delete")
    assert r.status_code in (302, 303)
    assert len(app.notes) == 1
    assert app.notes[0]["title"] == "Note 1"


def test_delete_get_returns_405(client, app):
    _seed(app, 1)
    r = client.get("/notes/0/delete")
    assert r.status_code == 405


def test_delete_nonexistent_returns_404(client, app):
    _seed(app, 1)
    r = client.post("/notes/99/delete")
    assert r.status_code == 404


def test_homepage_has_delete_form(client, app):
    _seed(app, 1)
    r = client.get("/")
    body = r.data.decode()
    # Some form posting to the delete URL should appear.
    assert "/notes/0/delete" in body
