"""Acceptance tests for TASK 02 — delete a note."""


def _seed(app, n=2):
    # Helper that populates app.notes with n predictably-named test notes.
    # app.notes.clear() ensures we start from a known state every time —
    # a test that depends on prior state is fragile and hard to debug.
    # The notes have no "tags" key intentionally, mirroring legacy notes that
    # pre-date the tags feature; the delete route must not break on them.
    app.notes.clear()
    for i in range(n):
        app.notes.append({"title": f"Note {i}", "body": f"Body {i}"})


def test_delete_removes_note(client, app):
    # After deleting the note at index 0, the list should shrink by one
    # and "Note 1" (previously at index 1) should now be the only note.
    # This checks both the side-effect (list length changed) and that the
    # correct item was removed (not the wrong one).
    _seed(app, 2)
    r = client.post("/notes/0/delete")
    assert r.status_code in (302, 303)  # redirect back to home after delete
    assert len(app.notes) == 1
    assert app.notes[0]["title"] == "Note 1"


def test_delete_get_returns_405(client, app):
    # Deletion must only be triggered by a POST request, never a GET.
    # This matters because browsers prefetch links (GET), search-engine
    # crawlers follow links, and users can accidentally load a URL — all
    # of which would silently delete data if GET were allowed.
    # HTTP 405 Method Not Allowed is the correct response for the wrong verb.
    _seed(app, 1)
    r = client.get("/notes/0/delete")
    assert r.status_code == 405


def test_delete_nonexistent_returns_404(client, app):
    # Attempting to delete an index that doesn't exist should return
    # 404 Not Found, not a 500 Internal Server Error (which would mean
    # an unhandled exception) and not a silent 200 (which would hide the bug).
    # This guards against off-by-one errors and stale UI links.
    _seed(app, 1)
    r = client.post("/notes/99/delete")
    assert r.status_code == 404


def test_homepage_has_delete_form(client, app):
    # The home page must render a <form> that POSTs to the delete URL for
    # each note. Without this the delete route is correct but unreachable
    # through the normal UI — the feature is incomplete.
    _seed(app, 1)
    r = client.get("/")
    body = r.data.decode()
    # Some form posting to the delete URL should appear.
    assert "/notes/0/delete" in body
