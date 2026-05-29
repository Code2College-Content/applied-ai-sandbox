"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import functools

from flask import Flask, render_template, request, redirect, url_for, session, flash


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]
    app.users: dict[str, str] = {}  # username → password (plaintext, sandbox only)

    def login_required(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if "username" not in session:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return wrapped

    @app.route("/")
    @login_required
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            if not username or not password:
                error = "Username and password are required."
            elif username in app.users:
                error = "Username already taken."
            else:
                app.users[username] = password
                session["username"] = username
                return redirect(url_for("home"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            if app.users.get(username) == password and username:
                session["username"] = username
                return redirect(url_for("home"))
            error = "Invalid username or password."
        return render_template("login.html", error=error)

    @app.route("/logout", methods=["POST"])
    def logout():
        session.pop("username", None)
        return redirect(url_for("login"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
