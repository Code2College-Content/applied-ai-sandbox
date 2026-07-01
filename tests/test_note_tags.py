"""Tests for tag-chip rendering on the home page."""

import models


def _seed(app, notes):
    user = models.get_user_by_username(app, app.config["USERNAME"])
    app.notes.clear()
    for note in notes:
        note = dict(note)
        note.setdefault("owner_id", user.id)
        app.notes.append(note)


def test_no_tags_renders_no_chips(client, app):
    _seed(app, [{"title": "Plain", "body": "no tags here", "tags": []}])
    r = client.get("/")
    body = r.data.decode()
    assert 'class="chip"' not in body


def test_missing_tags_key_renders_no_chips(client, app):
    _seed(app, [{"title": "Plain", "body": "no tags key at all"}])
    r = client.get("/")
    assert b'class="chip"' not in r.data


def test_tags_render_as_chips(client, app):
    _seed(app, [{"title": "Tagged", "body": "x", "tags": ["personal", "work"]}])
    r = client.get("/")
    body = r.data.decode()
    assert body.count('class="chip"') == 2
    assert ">personal<" in body
    assert ">work<" in body
