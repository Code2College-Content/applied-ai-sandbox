"""Acceptance tests for the note search feature."""


def _seed(app):
    app.notes.clear()
    app.notes.extend(
        [
            {"title": "Work note", "body": "This is work related."},
            {"title": "Personal", "body": "Favorite hobbies are gardening."},
            {"title": "Shopping", "body": "Buy milk and bread."},
        ]
    )


def test_search_filters_by_title_or_body(client, app):
    _seed(app)

    r = client.get("/?q=work")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Work note" in body
    assert "Personal" not in body
    assert "Shopping" not in body


def test_search_is_case_insensitive(client, app):
    _seed(app)

    r = client.get("/?q=WORK")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Work note" in body


def test_search_strips_whitespace_before_matching(client, app):
    _seed(app)

    r = client.get("/?q= work ")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Work note" in body
    assert "Personal" not in body


def test_homepage_without_query_shows_all_notes(client, app):
    _seed(app)

    r = client.get("/")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Work note" in body
    assert "Personal" in body
    assert "Shopping" in body


def test_search_field_preserves_query_value(client, app):
    _seed(app)

    r = client.get("/?q=work")
    assert r.status_code == 200
    assert 'value="work"' in r.data.decode()
