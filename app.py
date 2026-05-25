"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for


def parse_tags(raw: str) -> list[str]:
    """Split a comma-separated string into a clean list of tag strings.

    Trims whitespace from each token and drops empty values.
    """
    return [tag for tag in (t.strip() for t in raw.split(",")) if tag]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            if not title:
                return render_template("new_note.html", error="Title is required",
                title=request.form.get("title"), body=request.form.get("body"))
            if not body:
                return render_template("new_note.html", error="Body is required",
                title=request.form.get("title"), body=request.form.get("body"))
            # TASK 01 will add validation here.
            tags = parse_tags(request.form.get("tags") or "")
            app.notes.append({"title": title, "body": body, "tags": tags})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
