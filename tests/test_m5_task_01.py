"""Acceptance test for M5 Task 1 — comma-separated tags on new-note form."""


def test_tags_parsed_from_form(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": "work, urgent"})
    assert app.notes[-1]["tags"] == ["work", "urgent"]
