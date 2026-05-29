"""Acceptance tests for TASK 03 — tags field on notes."""


def test_new_note_defaults_to_empty_tags(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "No Tags", "body": "Some body"})
    assert app.notes[-1]["tags"] == []
