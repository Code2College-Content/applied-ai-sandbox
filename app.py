"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations
import os

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    init_db,
)


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="sandbox-not-a-real-secret",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return get_user_by_id(user_id)

    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    @login_required
    def home():
        notes = [
            (idx, note)
            for idx, note in enumerate(app.notes)
            if note["owner"] == current_user.get_id()
        ]
        return render_template("home.html", notes=notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            error = None

            if not title:
                error = "Title is required"
            elif not body:
                error = "Body is required"

            if error:
                return render_template(
                    "new_note.html",
                    title=title,
                    body=body,
                    error=error,
                )

            app.notes.append(
                {
                    "title": title,
                    "body": body,
                    "owner": current_user.get_id(),
                }
            )
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:idx>/delete", methods=["POST"])
    @login_required
    def delete_note(idx):
        try:
            note = app.notes[idx]
        except IndexError:
            abort(404)
        if note["owner"] != current_user.get_id():
            abort(404)
        app.notes.pop(idx)
        return redirect(url_for("home"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = (request.form.get("password") or "").strip()
            confirm = (request.form.get("confirm") or "").strip()

            if not username:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            elif password != confirm:
                error = "Passwords must match"
            elif get_user_by_username(username) is not None:
                error = "Username already taken"
            else:
                user = create_user(username, generate_password_hash(password))
                login_user(user)
                return redirect(url_for("home"))

        return render_template(
            "register.html",
            error=error,
            username=request.form.get("username", ""),
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = (request.form.get("password") or "").strip()

            if not username or not password:
                error = "Username and password required"
            else:
                user_data = get_user_by_username(username)
                if user_data is None:
                    error = "Invalid username or password"
                else:
                    user, password_hash = user_data
                    if not check_password_hash(password_hash, password):
                        error = "Invalid username or password"
                    else:
                        login_user(user)
                        next_page = request.args.get("next")
                        if not next_page or not next_page.startswith("/"):
                            next_page = url_for("home")
                        return redirect(next_page)

        return render_template(
            "login.html",
            error=error,
            username=request.form.get("username", ""),
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
