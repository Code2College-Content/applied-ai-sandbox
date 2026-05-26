# conftest.py is a special pytest file — pytest discovers and loads it
# automatically before running any tests in the same directory.
# Fixtures defined here are shared across all test files without needing
# explicit imports — pytest injects them by matching parameter names.

import pytest
from app import create_app


@pytest.fixture
def app():
    # Create a fresh app instance for every test that requests this fixture.
    # Because create_app() initialises app.notes = [], each test starts
    # with an empty notes list — preventing state leaking between tests.
    # This is why we use the app factory pattern in app.py rather than a
    # module-level Flask instance.
    app = create_app()
    app.config["TESTING"] = True
    # TESTING = True tells Flask to propagate exceptions instead of catching
    # them and returning a 500 error page. This gives us clear tracebacks
    # in test output rather than cryptic HTTP 500 failures.
    return app


@pytest.fixture
def client(app):
    # app.test_client() returns a fake HTTP client that sends requests
    # directly to the Flask app without starting a real network server.
    # Tests call client.get("/"), client.post("/notes/new", data={...}), etc.
    # The 'app' parameter is automatically injected by pytest using the
    # fixture above — pytest resolves fixture dependencies by name.
    return app.test_client()
