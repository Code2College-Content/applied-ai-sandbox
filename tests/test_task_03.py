"""Acceptance tests for TASK 03 — tags (M5).

Task 2 of the M5 decomposition: the parse_tags helper. Step 7 later extends
this file with the save-path and filter tests. Don't edit existing tests to
make them pass — change app.py / templates instead.
"""
from app import parse_tags


def test_parse_tags_basic():
    assert parse_tags("work, urgent") == ["work", "urgent"]


def test_parse_tags_trims_and_drops_empties():
    # The M5 Task 2 verification example.
    assert parse_tags("work, , urgent ") == ["work", "urgent"]


def test_parse_tags_empty_string_returns_empty_list():
    assert parse_tags("") == []


def test_parse_tags_none_returns_empty_list():
    assert parse_tags(None) == []


def test_parse_tags_preserves_order_and_duplicates():
    assert parse_tags("b, a, a") == ["b", "a", "a"]


# --- Task 3: tags wired into the new-note form ---


def test_post_stores_parsed_tags(client, app):
    app.notes.clear()
    r = client.post(
        "/notes/new", data={"title": "T", "body": "B", "tags": "work, urgent"}
    )
    assert r.status_code in (302, 303)
    assert app.notes[-1]["tags"] == ["work", "urgent"]


def test_post_empty_tags_stores_empty_list(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": ""})
    assert app.notes[-1]["tags"] == []


def test_failed_submit_keeps_typed_tags(client):
    r = client.post(
        "/notes/new", data={"title": "", "body": "B", "tags": "work, urgent"}
    )
    assert r.status_code == 200
    assert b"work, urgent" in r.data
