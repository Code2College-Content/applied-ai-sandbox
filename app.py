"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import functools

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory stores for the sandbox. Reset on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]
    app.users: dict[str, str] = {}  # type: ignore[attr-defined]  # username → hashed pw

    # ------------------------------------------------------------------
    # Auth helpers
    # ------------------------------------------------------------------

    def login_required(view):
        """Redirect to /login if the user is not logged in."""
        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("username"):
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    # ------------------------------------------------------------------
    # Auth routes
    # ------------------------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if session.get("username"):
            return redirect(url_for("home"))
        error = None
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
                flash("Account created — welcome!", "success")
                return redirect(url_for("home"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if session.get("username"):
            return redirect(url_for("home"))
        error = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            hashed = app.users.get(username)
            if not hashed or not check_password_hash(hashed, password):
                error = "Invalid username or password."
            else:
                session["username"] = username
                return redirect(url_for("home"))
        return render_template("login.html", error=error)

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("login"))

    # ------------------------------------------------------------------
    # App routes
    # ------------------------------------------------------------------

    @app.route("/")
    @login_required
    def home():
        username = session["username"]
        return render_template("home.html", notes=app.notes, username=username)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        error = None
        title = ""
        body = ""
        tags_raw = ""
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            tags_raw = (request.form.get("tags") or "").strip()
            if not title:
                error = "Title is required"
            elif not body:
                error = "Body is required"
            else:
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
                app.notes.append({"title": title, "body": body, "tags": tags})
                return redirect(url_for("home"))
        return render_template("new_note.html", error=error, title=title, body=body, tags=tags_raw)

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
