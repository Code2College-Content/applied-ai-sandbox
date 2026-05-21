from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    app.notes = []

    @app.route("/")
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            tags = [tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()]
            app.notes.append({"title": title, "body": body, "tags": tags, "likes": 0, "liked": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/like", methods=["POST"])
    def like_note(idx: int):
        if 0 <= idx < len(app.notes):
            note = app.notes[idx]
            if not note.get("liked", False):
                note["likes"] = note.get("likes", 0) + 1
                note["liked"] = True
        return redirect(url_for("home"))

    @app.route("/notes/<int:idx>/unlike", methods=["POST"])
    def unlike_note(idx: int):
        if 0 <= idx < len(app.notes):
            note = app.notes[idx]
            if note.get("liked", False):
                note["likes"] = max(0, note.get("likes", 0) - 1)
                note["liked"] = False
        return redirect(url_for("home"))

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)