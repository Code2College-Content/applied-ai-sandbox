"""Tiny Flask app — applied-ai-sandbox."""
from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            errors = {}
            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"
            if errors:
                return render_template("new_note.html", errors=errors, title=title, body=body)
            app.notes.append({"title": title, "body": body, "tags": []})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)