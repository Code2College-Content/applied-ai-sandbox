import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        with app.test_request_context():
            pass
        # register and log in
        c.post("/register", data={"username": "tester", "password": "pw"})
        yield c, app


def _add_note(client, title="T", body="B", tags=""):
    client.post("/notes/new", data={"title": title, "body": body, "tags": tags})


def test_new_note_defaults_starred_false(client):
    c, app = client
    _add_note(c)
    assert app.notes[0].get("starred") is False


def test_star_toggles_to_true(client):
    c, app = client
    _add_note(c)
    c.post("/notes/0/star")
    assert app.notes[0]["starred"] is True


def test_star_toggles_back_to_false(client):
    c, app = client
    _add_note(c)
    c.post("/notes/0/star")
    c.post("/notes/0/star")
    assert app.notes[0]["starred"] is False


def test_home_unfiltered_shows_all(client):
    c, app = client
    _add_note(c, title="A")
    _add_note(c, title="B")
    c.post("/notes/0/star")
    rv = c.get("/")
    assert b"A" in rv.data
    assert b"B" in rv.data


def test_home_starred_filter_shows_only_starred(client):
    c, app = client
    _add_note(c, title="Starred")
    _add_note(c, title="Unstarred")
    c.post("/notes/0/star")
    rv = c.get("/?starred=1")
    assert b"Starred" in rv.data
    assert b"Unstarred" not in rv.data


def test_home_starred_filter_empty_message(client):
    c, app = client
    _add_note(c, title="Plain")
    rv = c.get("/?starred=1")
    assert b"No starred notes yet" in rv.data


def test_star_invalid_index_returns_404(client):
    c, app = client
    rv = c.post("/notes/999/star")
    assert rv.status_code == 404


def test_star_requires_login():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        rv = c.post("/notes/0/star")
        assert rv.status_code == 302
        assert "/login" in rv.headers["Location"]


def test_old_note_without_starred_key_handled(client):
    c, app = client
    # simulate a note created before the starred field was added
    app.notes.append({"title": "Old", "body": "legacy", "tags": []})
    rv = c.get("/")
    assert b"Old" in rv.data
    rv2 = c.get("/?starred=1")
    assert b"Old" not in rv2.data
