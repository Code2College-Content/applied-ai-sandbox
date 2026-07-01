"""Tests for note pinning — pinned notes float to the top of the list."""

import models


def _seed(app, notes):
    user = models.get_user_by_username(app, app.config["USERNAME"])
    app.notes.clear()
    for note in notes:
        note = dict(note)
        note.setdefault("owner_id", user.id)
        app.notes.append(note)


def test_note_without_pinned_key_renders_unpinned(client, app):
    _seed(app, [{"title": "Plain", "body": "x"}])
    r = client.get("/")
    assert r.status_code == 200
    assert b"Plain" in r.data


def test_toggle_pin_moves_note_to_top(client, app):
    _seed(app, [
        {"title": "First", "body": "x"},
        {"title": "Second", "body": "x"},
    ])
    r = client.post("/notes/1/pin")
    assert r.status_code in (302, 303)
    assert app.notes[1]["pinned"] is True

    body = client.get("/").data.decode()
    assert body.index("Second") < body.index("First")


def test_pinned_and_unpinned_groups_preserve_relative_order(client, app):
    # Distinct multi-char titles — avoids false substring matches against
    # static page text (e.g. a bare "A" would also match "...Applied AI...").
    _seed(app, [
        {"title": "NoteA", "body": "x"},
        {"title": "NoteB", "body": "x"},
        {"title": "NoteC", "body": "x"},
        {"title": "NoteD", "body": "x"},
    ])
    client.post("/notes/1/pin")  # pin NoteB
    client.post("/notes/3/pin")  # pin NoteD

    body = client.get("/").data.decode()
    positions = {t: body.index(t) for t in ("NoteA", "NoteB", "NoteC", "NoteD")}
    # pinned group (B, D) first, in original relative order; then unpinned (A, C)
    assert positions["NoteB"] < positions["NoteD"] < positions["NoteA"] < positions["NoteC"]


def test_unpin_returns_note_to_normal_position(client, app):
    _seed(app, [
        {"title": "First", "body": "x"},
        {"title": "Second", "body": "x"},
    ])
    client.post("/notes/1/pin")
    client.post("/notes/1/pin")  # toggle back off
    assert app.notes[1]["pinned"] is False
    body = client.get("/").data.decode()
    assert body.index("First") < body.index("Second")


def test_pin_bad_index_returns_404(client, app):
    _seed(app, [{"title": "Only", "body": "x"}])
    r = client.post("/notes/99/pin")
    assert r.status_code == 404


def test_pin_get_returns_405(client, app):
    _seed(app, [{"title": "Only", "body": "x"}])
    r = client.get("/notes/0/pin")
    assert r.status_code == 405
