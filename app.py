"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for


def parse_tags(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        notes = app.notes
        q = request.args.get("q", "").strip().lower()
        show_starred = request.args.get("starred") == "1"
        if show_starred:
            notes = [n for n in notes if n.get("starred")]
        if q:
            notes = [n for n in notes if q in n["title"].lower() or q in n["body"].lower()]
        return render_template("home.html", notes=notes, q=q, show_starred=show_starred)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            tags = parse_tags(request.form.get("tags") or "")
            # TASK 01 will add validation here.
            idx = len(app.notes)
            app.notes.append({
                "id": idx,
                "title": title,
                "body": body,
                "tags": tags,
                "starred": False,
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            })
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def toggle_star(idx):
        note = app.notes[idx]
        note["starred"] = not note.get("starred", False)
        note["updatedAt"] = datetime.now(timezone.utc).isoformat()
        return redirect(url_for("home", **request.args))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
