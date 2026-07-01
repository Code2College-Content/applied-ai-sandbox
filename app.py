"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import os

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import models


def create_app(database: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    app.config["DATABASE"] = database or os.path.join(app.root_path, "sandbox.db")

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    models.init_db(app)
    # Seed the sandbox's original default account so it keeps working as a
    # login for anyone following older instructions/tests.
    default_username = os.environ.get("APP_USERNAME", "admin")
    default_password = os.environ.get("APP_PASSWORD", "password")
    app.config["USERNAME"] = default_username
    if models.get_user_by_username(app, default_username) is None:
        models.create_user(app, default_username, default_password)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.get_user_by_id(app, user_id)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            user = models.get_user_by_username(app, username)
            if user is None or not user.check_password(password):
                return render_template("login.html", error="Invalid username or password", username=username)
            login_user(user)
            return redirect(url_for("home"))
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            error = None
            if not username:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            elif models.get_user_by_username(app, username) is not None:
                error = "That username is already taken"
            if error:
                return render_template("register.html", error=error, username=username)
            user = models.create_user(app, username, password)
            login_user(user)
            return redirect(url_for("home"))
        return render_template("register.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def home():
        my_notes = [
            dict(n, idx=i)
            for i, n in enumerate(app.notes)
            if n.get("owner_id") == current_user.id
        ]
        my_notes.sort(key=lambda n: 0 if n.get("pinned", False) else 1)
        return render_template("home.html", notes=my_notes, username=current_user.username)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "owner_id": current_user.id})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/pin", methods=["POST"])
    @login_required
    def toggle_pin(idx):
        if idx < 0 or idx >= len(app.notes) or app.notes[idx].get("owner_id") != current_user.id:
            abort(404)
        app.notes[idx]["pinned"] = not app.notes[idx].get("pinned", False)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
