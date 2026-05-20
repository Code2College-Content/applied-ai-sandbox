"""Tiny Flask app — applied-ai-sandbox."""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    app.notes: list[dict] = []  # in-memory store

    @app.route("/")
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()

            if not title:
                return render_template(
                    "new_note.html",
                    error="Title is required",
                    title=title,
                    body=body,
                )

            if not body:
                return render_template(
                    "new_note.html",
                    error="Body is required",
                    title=title,
                    body=body,
                )

            app.notes.append({"title": title, "body": body})
            return redirect(url_for("home"))

        return render_template("new_note.html")

    # ✅ TASK 02: DELETE ROUTE
    @app.route("/notes/<int:idx>/delete", methods=["POST"])
    def delete_note(idx: int):
        # must return 404 for invalid index
        if idx < 0 or idx >= len(app.notes):
            abort(404)

        app.notes.pop(idx)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)