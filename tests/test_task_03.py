"""Acceptance tests for TASK 03 — search notes."""


def _seed(app):
    app.notes.clear()
    app.notes.append({"title": "Flask intro", "body": "All about Flask"})
    app.notes.append({"title": "Python basics", "body": "Variables and loops"})


def test_search_filters_by_title(client, app):
    _seed(app)
    r = client.get("/?q=flask")
    body = r.data.decode()
    assert "Flask intro" in body
    assert "Python basics" not in body


def test_search_filters_by_body(client, app):
    _seed(app)
    r = client.get("/?q=loops")
    body = r.data.decode()
    assert "Python basics" in body
    assert "Flask intro" not in body


def test_search_is_case_insensitive(client, app):
    _seed(app)
    r = client.get("/?q=FLASK")
    body = r.data.decode()
    assert "Flask intro" in body


def test_no_query_returns_all(client, app):
    _seed(app)
    r = client.get("/")
    body = r.data.decode()
    assert "Flask intro" in body
    assert "Python basics" in body


def test_empty_query_returns_all(client, app):
    _seed(app)
    r = client.get("/?q=")
    body = r.data.decode()
    assert "Flask intro" in body
    assert "Python basics" in body


def test_no_results_shows_message(client, app):
    _seed(app)
    r = client.get("/?q=xyz")
    body = r.data.decode()
    assert "No notes found" in body


def test_search_form_present(client, app):
    r = client.get("/")
    body = r.data.decode()
    assert 'name="q"' in body
