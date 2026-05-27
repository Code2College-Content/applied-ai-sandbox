"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        filter_starred = request.args.get("starred") == "1"
        indexed = [(i, n) for i, n in enumerate(app.notes) if n["starred"]] if filter_starred else list(enumerate(app.notes))
        return render_template("home.html", indexed=indexed, filter_starred=filter_starred)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            raw_tags = (request.form.get("tags") or "").strip()
            tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "tags": tags, "starred": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def star_note(idx):
        try:
            note = app.notes[idx]
        except IndexError:
            abort(404)
        note["starred"] = not note["starred"]
        return redirect(url_for("home"))

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
