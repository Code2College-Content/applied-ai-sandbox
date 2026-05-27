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
        pinned = [(i, n) for i, n in enumerate(app.notes) if n.get("pinned", False)]
        unpinned = [(i, n) for i, n in enumerate(app.notes) if not n.get("pinned", False)]
        return render_template("home.html", pinned=pinned, unpinned=unpinned)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "pinned": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/pin", methods=["POST"])
    def pin_note(idx):
        try:
            app.notes[idx]["pinned"] = not app.notes[idx].get("pinned", False)
        except IndexError:
            abort(404)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
