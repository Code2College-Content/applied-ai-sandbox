from __future__ import annotations

import sqlite3
from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: int, username: str):
        self.id = str(id)
        self.username = username

    def get_id(self) -> str:
        return self.id


def get_db() -> sqlite3.Connection:
    db = sqlite3.connect(current_app.config["DATABASE"])
    db.row_factory = sqlite3.Row
    return db


def init_db(app) -> None:
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        db.commit()


def get_user_by_id(user_id: str) -> User | None:
    db = get_db()
    row = db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    return User(row["id"], row["username"]) if row else None


def get_user_by_username(username: str) -> tuple[User, str] | None:
    db = get_db()
    row = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if not row:
        return None
    return User(row["id"], row["username"]), row["password_hash"]


def create_user(username: str, password_hash: str) -> User:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    db.commit()
    user_id = cursor.lastrowid
    return User(user_id, username)
