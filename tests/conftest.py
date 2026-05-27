import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """A test client pre-logged-in as the test user."""
    c = app.test_client()
    # Register and log in a test user so auth-protected routes work in tests.
    c.post("/register", data={"username": "testuser", "password": "testpass"})
    return c
