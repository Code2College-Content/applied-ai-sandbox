from __future__ import annotations

import sqlite3

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str) -> None:
        self.id = id
        self.username = username
        self.password_hash = password_hash


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                password_hash TEXT    NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def find_by_username(db_path: str, username: str) -> User | None:
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    finally:
        conn.close()
    return User(row["id"], row["username"], row["password_hash"]) if row else None


def find_by_id(db_path: str, user_id: int) -> User | None:
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()
    return User(row["id"], row["username"], row["password_hash"]) if row else None


def create_user(db_path: str, username: str, password_hash: str) -> User:
    conn = _connect(db_path)
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid
    finally:
        conn.close()
    return User(user_id, username, password_hash)
