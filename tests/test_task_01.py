"""Acceptance tests for TASK 01 — validate the new-note form.

Don't edit these to make them pass. Change app.py / templates instead.

These tests define the contract for the new-note feature:
  - Required fields must be enforced server-side (never trust client-side only).
  - Validation errors must be shown inline without losing the user's typed input.
  - A successful submission must redirect and actually save the note.
"""


def test_empty_title_shows_error(client):
    # POST the form with an empty title to simulate a user forgetting to fill it in.
    # Expected: stay on the form page (200 OK — not a redirect) and include the
    # error message text in the HTML so the user knows exactly what to fix.
    r = client.post("/notes/new", data={"title": "", "body": "hi"})
    assert r.status_code == 200           # still on the form, not redirected
    assert b"Title is required" in r.data  # error message visible in the page


def test_empty_body_shows_error(client):
    # Same validation contract for the body field.
    # Each required field gets its own specific error message so users
    # know which field to fix rather than getting a generic "form invalid".
    r = client.post("/notes/new", data={"title": "Hello", "body": ""})
    assert r.status_code == 200
    assert b"Body is required" in r.data


def test_valid_submit_redirects_and_persists(client, app):
    # A valid submission (both fields filled in) should do two things:
    # 1. Return a redirect (302 or 303) — this is the Post/Redirect/Get (PRG)
    #    pattern. Without a redirect, refreshing the confirmation page would
    #    re-submit the form and create duplicate notes.
    # 2. Actually store the note in app.notes so it survives the redirect
    #    and appears on the home page.
    app.notes.clear()  # start from zero so we know exactly what's in the list
    r = client.post(
        "/notes/new", data={"title": "First", "body": "Hello world"},
    )
    assert r.status_code in (302, 303)                    # redirect issued
    assert any(n["title"] == "First" for n in app.notes)  # note was saved


def test_invalid_submit_preserves_typed_values(client):
    # When validation fails the user's already-typed values must be echoed
    # back into the form fields. Without this, users lose their work on every
    # mistake — a frustrating UX that's easy to accidentally omit.
    # We check the title because that's what was typed before submitting.
    r = client.post("/notes/new", data={"title": "Half typed", "body": ""})
    assert r.status_code == 200
    # User's typed-in title should still be in the rendered form
    assert b"Half typed" in r.data
