"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import re

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape, Markup


def _highlight(text: str, query: str) -> Markup:
    """Return first 150 chars of text with query matches wrapped in <mark>."""
    snippet = (text or "")[:150]
    escaped = str(escape(snippet))
    marked = re.sub(
        re.escape(query),
        lambda m: f"<mark>{m.group()}</mark>",
        escaped,
        flags=re.IGNORECASE,
    )
    return Markup(marked)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        q = request.args.get("q", "")
        return render_template("home.html", notes=app.notes, q=q)

    @app.route("/search")
    def search():
        q = (request.args.get("q") or "").strip()
        if not q:
            return redirect(url_for("home"))
        ql = q.lower()
        results = []
        for note in app.notes:
            title = (note.get("title") or "")
            body = (note.get("body") or "")
            if ql in title.lower() or ql in body.lower():
                results.append({
                    "title": title,
                    "snippet": _highlight(body, ql),
                })
        return render_template(
            "search.html",
            results=results,
            query=q,
            count=len(results),
            total=len(app.notes),
        )

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "tags": []})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
