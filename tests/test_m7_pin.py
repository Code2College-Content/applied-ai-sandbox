"""Acceptance tests for M7 — note pinning.

Don't edit these to make them pass. Change app.py / templates instead.
"""


def _seed(app, n=2):
    app.notes.clear()
    for i in range(n):
        app.notes.append({"title": f"Note {i}", "body": f"Body {i}", "pinned": False})


def test_pin_toggles_pinned_true(client, app):
    _seed(app, 1)
    r = client.post("/notes/0/pin")
    assert r.status_code in (302, 303)
    assert app.notes[0]["pinned"] is True


def test_pin_toggles_pinned_back_to_false(client, app):
    _seed(app, 1)
    app.notes[0]["pinned"] = True
    r = client.post("/notes/0/pin")
    assert r.status_code in (302, 303)
    assert app.notes[0]["pinned"] is False


def test_pin_get_returns_405(client, app):
    _seed(app, 1)
    r = client.get("/notes/0/pin")
    assert r.status_code == 405


def test_pin_nonexistent_returns_404(client, app):
    _seed(app, 1)
    r = client.post("/notes/99/pin")
    assert r.status_code == 404


def test_pinned_note_appears_before_unpinned_in_html(client, app):
    _seed(app, 2)
    app.notes[1]["pinned"] = True  # pin the second note (storage idx 1)
    r = client.get("/")
    body = r.data.decode()
    assert body.index("Note 1") < body.index("Note 0")


def test_homepage_has_pin_form(client, app):
    _seed(app, 1)
    r = client.get("/")
    assert b"/notes/0/pin" in r.data


def test_new_note_defaults_pinned_false(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B"})
    assert app.notes[0].get("pinned") is False
