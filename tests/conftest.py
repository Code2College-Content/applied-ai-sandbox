import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from models import create_user

TEST_USER = "testuser"
TEST_PASS = "testpass"


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    application = create_app({"DATABASE": db_path, "TESTING": True})
    create_user(db_path, TEST_USER, generate_password_hash(TEST_PASS))
    yield application
    os.close(db_fd)
    try:
        os.unlink(db_path)
    except OSError:
        pass  # Windows may lock the file; temp dir cleans it up eventually


@pytest.fixture
def client(app):
    c = app.test_client()
    c.post("/login", data={"username": TEST_USER, "password": TEST_PASS})
    return c
