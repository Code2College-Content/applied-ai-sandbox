"""Acceptance tests for TASK 03 — optional date field on notes.

Don't edit these to make them pass. Change app.py / templates instead.
"""


def test_note_without_date_has_none(client, app):
    """When no date is submitted, note.date is None."""
    app.notes.clear()
    client.post("/notes/new", data={"title": "No Date", "body": "body text"})
    assert app.notes[0]["date"] is None


def test_note_with_date_persists(client, app):
    """When a date is submitted, it is stored on the note."""
    app.notes.clear()
    client.post("/notes/new", data={"title": "Dated", "body": "body", "date": "2026-06-01"})
    assert app.notes[0]["date"] == "2026-06-01"


def test_date_appears_on_homepage(client, app):
    """A note's date is rendered in the homepage HTML."""
    app.notes.clear()
    client.post("/notes/new", data={"title": "Show Date", "body": "body", "date": "2026-07-04"})
    r = client.get("/")
    assert b"2026-07-04" in r.data


def test_no_date_not_shown_on_homepage(client, app):
    """A note without a date does not render a date element."""
    app.notes.clear()
    client.post("/notes/new", data={"title": "No Date Note", "body": "body"})
    r = client.get("/")
    assert b"note-date" not in r.data
