import os
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from models import create_user, init_db


@pytest.fixture
def app(tmp_path: Path):
    test_db = tmp_path / "app.sqlite"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(test_db),
        }
    )
    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        init_db(app)
        create_user("testuser", generate_password_hash("secret"))
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class AuthActions:
        def login(self, username="testuser", password="secret"):
            return client.post(
                "/login", data={"username": username, "password": password}
            )

        def logout(self):
            return client.get("/logout")

    return AuthActions()
