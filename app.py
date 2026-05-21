"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import create_user, find_by_id, find_by_username, init_db


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    app.config["DATABASE"] = "sandbox.db"
    if config:
        app.config.update(config)

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Each note carries a user_id field for per-user filtering.
    app.notes: list = []  # type: ignore[attr-defined]

    login_manager = LoginManager(app)
    login_manager.login_view = "login"  # type: ignore[assignment]

    @login_manager.user_loader
    def load_user(user_id: str):
        return find_by_id(app.config["DATABASE"], int(user_id))

    init_db(app.config["DATABASE"])

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                error = "Username and password are required"
            elif find_by_username(app.config["DATABASE"], username):
                error = "Username already taken"
            else:
                create_user(
                    app.config["DATABASE"],
                    username,
                    generate_password_hash(password),
                )
                return redirect(url_for("login"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = find_by_username(app.config["DATABASE"], username)
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("home"))
            error = "Invalid username or password"
        return render_template("login.html", error=error)

    @app.route("/logout", methods=["POST"])
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def home():
        notes = [
            n for n in app.notes
            if n.get("user_id") is None or n.get("user_id") == current_user.id
        ]
        return render_template("home.html", notes=notes, username=current_user.username)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "user_id": current_user.id})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
