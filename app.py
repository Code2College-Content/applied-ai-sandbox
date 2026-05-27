"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import functools

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    if config:
        app.config.update(config)

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    # In-memory user store: { username: hashed_password }
    app.users: dict[str, str] = {}  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Auth helpers
    # ------------------------------------------------------------------

    def login_required(f):
        """Redirect to /login if the user is not logged in."""
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if "username" not in session:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return wrapper

    # ------------------------------------------------------------------
    # Auth routes
    # ------------------------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        username = ""
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            if not username:
                error = "Username is required."
            elif not password:
                error = "Password is required."
            elif username in app.users:
                error = "That username is already taken."
            else:
                app.users[username] = generate_password_hash(password)
                session["username"] = username
                return redirect(url_for("home"))
        return render_template("register.html", error=error, username=username)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        username = ""
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            hashed = app.users.get(username)
            if not hashed or not check_password_hash(hashed, password):
                error = "Invalid username or password."
            else:
                session["username"] = username
                return redirect(url_for("home"))
        return render_template("login.html", error=error, username=username)

    @app.route("/logout", methods=["POST"])
    def logout():
        session.pop("username", None)
        return redirect(url_for("login"))

    # ------------------------------------------------------------------
    # App routes (all protected)
    # ------------------------------------------------------------------

    @app.route("/")
    @login_required
    def home():
        return render_template("home.html", notes=app.notes, username=session["username"])

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        error = None
        title = ""
        body = ""
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            if not title:
                error = "Title is required."
            else:
                app.notes.append({"title": title, "body": body, "tags": []})
                return redirect(url_for("home"))
        return render_template("new_note.html", error=error, title=title, body=body)

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)

def average_rating(ratings):
    if not ratings:
        return None
    return sum(ratings) / len(ratings)
