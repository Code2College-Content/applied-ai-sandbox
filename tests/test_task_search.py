"""Acceptance tests for note search — GET /notes endpoint."""

import json


def _seed(app, notes):
    app.notes.clear()
    for n in notes:
        app.notes.append(n)


def _get(client, **params):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"/notes?{qs}" if qs else "/notes"
    r = client.get(url)
    return r, json.loads(r.data)


def test_no_q_returns_all(client, app):
    _seed(app, [
        {"title": "Alpha", "body": "one"},
        {"title": "Beta",  "body": "two"},
    ])
    r, data = _get(client)
    assert r.status_code == 200
    assert data["total_count"] == 2
    assert data["query"] == ""


def test_q_filters_by_title(client, app):
    _seed(app, [
        {"title": "Flask tips", "body": "some content"},
        {"title": "Python basics", "body": "other content"},
    ])
    r, data = _get(client, q="Flask")
    assert r.status_code == 200
    assert data["total_count"] == 1
    assert data["notes"][0]["title"] == "Flask tips"


def test_q_filters_by_body(client, app):
    _seed(app, [
        {"title": "Note A", "body": "contains searchterm here"},
        {"title": "Note B", "body": "nothing relevant"},
    ])
    r, data = _get(client, q="searchterm")
    assert r.status_code == 200
    assert data["total_count"] == 1
    note = data["notes"][0]
    assert note["matched_in"] == "body"
    assert note["snippet"] is not None
    assert "searchterm" in note["snippet"].lower()


def test_matched_in_both(client, app):
    _seed(app, [{"title": "keyword title", "body": "body has keyword too"}])
    r, data = _get(client, q="keyword")
    assert r.status_code == 200
    assert data["notes"][0]["matched_in"] == "both"


def test_whitespace_q_returns_all(client, app):
    _seed(app, [{"title": "X", "body": "y"}, {"title": "A", "body": "b"}])
    r, data = _get(client, q="   ")
    assert r.status_code == 200
    assert data["total_count"] == 2
    assert data["query"] == ""


def test_long_q_returns_400(client, app):
    _seed(app, [])
    r, data = _get(client, q="a" * 201)
    assert r.status_code == 400
    assert "error" in data


def test_total_count_and_query_fields(client, app):
    _seed(app, [{"title": "Hello world", "body": "content"}])
    r, data = _get(client, q="Hello")
    assert r.status_code == 200
    assert "total_count" in data
    assert "query" in data
    assert data["query"] == "Hello"


def test_pagination(client, app):
    _seed(app, [{"title": f"Note {i}", "body": "shared term"} for i in range(5)])
    r, data = _get(client, q="shared", page=2, limit=2)
    assert r.status_code == 200
    assert data["total_count"] == 5
    assert len(data["notes"]) == 2


def test_no_results_returns_empty_list(client, app):
    _seed(app, [{"title": "Alpha", "body": "content"}])
    r, data = _get(client, q="zzznomatch")
    assert r.status_code == 200
    assert data["total_count"] == 0
    assert data["notes"] == []


def test_missing_created_at_handled(client, app):
    _seed(app, [{"title": "Old note", "body": "no timestamp"}])
    r, data = _get(client)
    assert r.status_code == 200
    assert data["notes"][0]["created_at"] is None


def test_title_matches_rank_before_body_only(client, app):
    _seed(app, [
        {"title": "Unrelated", "body": "the target word appears here"},
        {"title": "target word in title", "body": "something else"},
    ])
    r, data = _get(client, q="target word")
    assert r.status_code == 200
    assert data["notes"][0]["matched_in"] in ("title", "both")


def test_case_insensitive_search(client, app):
    _seed(app, [{"title": "Flask Tips", "body": "content"}])
    r, data = _get(client, q="flask tips")
    assert r.status_code == 200
    assert data["total_count"] == 1


def test_limit_zero_clamped_to_one(client, app):
    _seed(app, [{"title": f"Note {i}", "body": "content"} for i in range(5)])
    r, data = _get(client, q="content", limit=0)
    assert r.status_code == 200
    assert len(data["notes"]) == 1
    assert data["total_count"] == 5


def test_limit_above_cap_clamped_to_100(client, app):
    _seed(app, [{"title": f"Note {i}", "body": "content"} for i in range(150)])
    r, data = _get(client, q="content", limit=200)
    assert r.status_code == 200
    assert len(data["notes"]) == 100
    assert data["total_count"] == 150


def test_page_out_of_range_returns_empty_notes_not_zero_total(client, app):
    _seed(app, [{"title": f"Note {i}", "body": "content"} for i in range(3)])
    r, data = _get(client, q="content", page=999)
    assert r.status_code == 200
    assert data["total_count"] == 3  # results exist — caller must not treat notes=[] as "no match"
    assert data["notes"] == []


def test_no_q_notes_have_null_matched_in_and_snippet(client, app):
    _seed(app, [{"title": "T", "body": "B"}])
    r, data = _get(client)
    assert r.status_code == 200
    note = data["notes"][0]
    assert note["matched_in"] is None
    assert note["snippet"] is None


def test_html_special_chars_in_title_returned_safely(client, app):
    xss_title = "<script>alert(1)</script>"
    xss_body = '<img src=x onerror="alert(2)">'
    _seed(app, [{"title": xss_title, "body": xss_body}])

    # /notes API: strings round-trip correctly through JSON serialisation
    r, data = _get(client)
    assert r.status_code == 200
    assert data["total_count"] == 1
    note = data["notes"][0]
    assert note["title"] == xss_title
    assert note["body"] == xss_body
    # The response is application/json, so browsers never interpret its body
    # as HTML — that is the API's XSS protection, not character escaping.
    assert "application/json" in r.content_type

    # Home page: Jinja2 auto-escaping must convert < / > so the raw HTML
    # response bytes cannot trigger script execution.
    home = client.get("/")
    assert home.status_code == 200
    assert b"<script>alert(1)</script>" not in home.data
    assert b"&lt;script&gt;" in home.data
