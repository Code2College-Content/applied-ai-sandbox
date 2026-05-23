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
        """
        Handle the creation of a new note.

        This route supports both GET and POST methods:
        - GET: Renders the form for creating a new note.
        - POST: Processes the form submission, creates a new note, and adds it to the app.notes list.

        The new note includes the following fields:
        - title (str): The title of the note, stripped of leading/trailing whitespace.
        - body (str): The body content of the note, stripped of leading/trailing whitespace.
        - tags (list[str]): A list of tags, parsed from a comma-separated string and stripped of whitespace.
        - likes (int): The number of likes for the note, initialized to 0.
        - liked (bool): Whether the note is liked by the current user, initialized to False.

        Returns:
            Response: 
            - If GET: Renders the "new_note.html" template.
            - If POST: Redirects to the home page after adding the new note.
        """
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
        """
        Like a note by its index.

        This route increments the "likes" count for the note at the given index
        and sets the "liked" status to True, if the note is not already liked.

        Args:
            idx (int): The index of the note in the app.notes list.

        Returns:
            Response: A redirect to the home page.
        """
        if 0 <= idx < len(app.notes):
            note = app.notes[idx]
            if not note.get("liked", False):
                note["likes"] = note.get("likes", 0) + 1
                note["liked"] = True
        return redirect(url_for("home"))

    @app.route("/notes/<int:idx>/unlike", methods=["POST"])
    def unlike_note(idx: int):
        """
        Unlike a note by its index.

        This route decrements the "likes" count for the note at the given index
        and sets the "liked" status to False, if the note is currently liked.
        The "likes" count will not go below zero.

        Args:
            idx (int): The index of the note in the app.notes list.

        Returns:
            Response: A redirect to the home page.
        """
        if 0 <= idx < len(app.notes):
            note = app.notes[idx]
            if note.get("liked", False):
                note["likes"] = max(0, note.get("likes", 0) - 1)
                note["liked"] = False
        return redirect(url_for("home"))

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)