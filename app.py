"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations
# Defers evaluation of type hints so we can write modern syntax like list[dict]
# even on Python 3.9, where that syntax isn't natively supported at runtime.

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort


def create_app() -> Flask:
    # The "app factory" pattern: wrap app creation in a function instead of
    # creating a module-level global. This means each call produces a fresh,
    # independent Flask instance — essential for test isolation, where every
    # test needs its own clean app.notes list with no leftover state.
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    # SECRET_KEY is required by Flask for cryptographically signing sessions
    # and flash messages. In production it must be a long random string stored
    # in an environment variable — never hardcoded in source code.

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    # Attaching notes to the app object (rather than a module-level list)
    # keeps each factory-created instance fully independent.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        # Read the optional ?tag= query parameter from the URL (e.g. /?tag=work).
        # request.args is a dict-like object of URL query parameters.
        # We normalize to lowercase so "Work" and "work" match the same notes —
        # tags are stored lowercase at write time, so this keeps filtering consistent.
        tag = request.args.get("tag", "").strip().lower()

        # If a tag filter is active, keep only notes whose tags list contains
        # that exact tag. .get("tags", []) handles legacy notes that were created
        # before the tags field existed — avoids a KeyError on older dicts.
        # If no filter is active (tag == ""), show all notes unchanged.
        notes_by_starred = sorted(app.notes, key=lambda n: not n.get("starred", False))
        notes = notes_by_starred if not tag else [
            n for n in notes_by_starred if tag in n.get("tags", [])
        ]

        # Build the sorted, deduplicated set of every tag across ALL notes
        # (not just the filtered subset), so the filter bar always shows
        # every available option regardless of the active filter.
        # Set comprehension naturally deduplicates; sorted() makes order predictable.
        all_tags = sorted({t for n in app.notes for t in n.get("tags", [])})

        # Pass three things to the template:
        #   notes     — the (possibly filtered) list to display
        #   all_tags  — every unique tag, for building the filter bar
        #   active_tag — which tag is currently selected (empty string = "All")
        return render_template("home.html", notes=notes, all_tags=all_tags, active_tag=tag)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        # This single route handles two HTTP methods:
        #   GET  — user navigated to the form; render it blank
        #   POST — user submitted the form; validate and save
        if request.method == "POST":
            # request.form is a dict-like object populated from the POST body.
            # "or ''" guards against None (field present but empty, or missing entirely).
            # .strip() removes accidental leading/trailing whitespace from user input.
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()

            # Keep the raw comma-separated string the user typed.
            # We preserve it here so it can be echoed back into the input field
            # unchanged if validation fails — users shouldn't lose their work.
            # Intentionally NOT parsed yet: raw_tags is for form refill only.
            raw_tags = (request.form.get("tags") or "").strip()

            # Validate required fields. None = no error; a string = error message text.
            title_error = "Title is required" if not title else None
            body_error  = "Body is required"  if not body  else None

            if title_error or body_error:
                # Re-render the form with the user's original input intact.
                # tags=raw_tags passes the raw string (not a list) because the
                # HTML <input value="..."> attribute expects a plain string.
                # This is why we keep raw_tags separate from the parsed list.
                return render_template("new_note.html", title=title, body=body,
                                       tags=raw_tags,
                                       title_error=title_error, body_error=body_error)

            # Parsing only happens after validation passes — the two concerns
            # (form refill vs. data storage) are intentionally kept separate.
            # Steps: split on commas → strip each piece → lowercase → drop empties.
            # Lowercasing at write time means filtering can always use exact match
            # without worrying about case mismatches later (e.g. "Work" vs "work").
            tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]

            # Store the note as a plain Python dict.
            # Keeping notes as dicts (rather than model objects) keeps the data
            # layer simple and explicit for this sandbox environment.
            app.notes.append({"title": title, "body": body, "tags": tags, "starred": False})

            # Redirect to home after a successful POST — this is the
            # Post/Redirect/Get (PRG) pattern. Without it, refreshing the
            # browser would re-submit the form and create duplicate notes.
            return redirect(url_for("home"))

        # GET request — render the blank form with no pre-filled values.
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    @app.route("/notes/<int:idx>/star", methods=["PATCH"])
    def star_note(idx):
        """Toggle the note's starred state and return the updated value."""
        if idx < 0 or idx >= len(app.notes):
            abort(404)
        note = app.notes[idx]
        note["starred"] = not note.get("starred", False)
        return jsonify({"starred": note["starred"]})

    return app


if __name__ == "__main__":
    # Only runs when the file is executed directly: python app.py
    # debug=True enables automatic reload on file changes and shows an
    # interactive debugger in the browser on errors.
    # NEVER use debug=True in production — it exposes a live Python shell.
    create_app().run(debug=True, port=5000)
