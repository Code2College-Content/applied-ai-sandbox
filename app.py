"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, session, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.before_request
    def load_user():
        app.user = session.get("username")

    @app.route("/")
    def home():
        q = request.args.get("q", "").strip()
        if q:
            notes = [
                n for n in app.notes
                if q.lower() in n["title"].lower() or q.lower() in n["body"].lower()
            ]
        else:
            notes = app.notes
        return render_template("home.html", notes=notes, user=app.user, q=q, total=len(app.notes))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        username = ""
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            if not username:
                error = "Username is required"
            else:
                session["username"] = username
                return redirect(url_for("home"))
        return render_template("login.html", error=error, username=username)

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("home"))

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        title = ""
        body = ""
        tags_raw = ""
        errors: dict[str, str] = {}

        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            tags_raw = (request.form.get("tags") or "").strip()
            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"
            if not errors:
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
                note = {"title": title, "body": body, "tags": tags}
                if app.user:
                    note["author"] = app.user
                app.notes.append(note)
                return redirect(url_for("home"))

        return render_template("new_note.html", title=title, body=body, tags_raw=tags_raw, errors=errors)

    @app.route("/notes/<int:idx>/delete", methods=["POST"])
    def delete_note(idx: int):
        try:
            del app.notes[idx]
        except IndexError:
            abort(404)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
