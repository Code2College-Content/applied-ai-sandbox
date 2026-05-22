"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

import html as _html
import re as _re

from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import create_user, find_by_id, find_by_username, init_db


def parse_tags(tag_string: str) -> list[str]:
    return [t.strip() for t in tag_string.split(",") if t.strip()]


def _highlight_terms(escaped_text: str, terms: list[str]) -> str:
    """Wrap matched terms in <mark> inside already-HTML-escaped text."""
    if not terms:
        return escaped_text
    pattern = "|".join(_re.escape(_html.escape(t)) for t in terms if t)
    if not pattern:
        return escaped_text
    return _re.sub(
        pattern, lambda m: f"<mark>{m.group()}</mark>", escaped_text, flags=_re.IGNORECASE
    )


def _make_snippet(body: str, terms: list[str], window: int = 160) -> str:
    """Return a highlighted body excerpt centred on the first term match."""
    escaped = _html.escape(body)
    pattern = "|".join(_re.escape(_html.escape(t)) for t in terms if t) if terms else ""
    m = _re.search(pattern, escaped, _re.IGNORECASE) if pattern else None

    if m:
        start = max(0, m.start() - window // 4)
        end = min(len(escaped), start + window)
        excerpt = escaped[start:end]
        prefix = "…" if start > 0 else ""
        suffix = "…" if end < len(escaped) else ""
    else:
        excerpt = escaped[:window]
        prefix = ""
        suffix = "…" if len(escaped) > window else ""

    highlighted = (
        _re.sub(pattern, lambda mo: f"<mark>{mo.group()}</mark>", excerpt, flags=_re.IGNORECASE)
        if pattern
        else excerpt
    )
    return prefix + highlighted + suffix


def _rank_note(note: dict, terms: list[str]) -> float:
    """Title matches weight 2×, body matches weight 1×."""
    title = (note.get("title") or "").lower()
    body = (note.get("body") or "").lower()
    score = 0.0
    for t in terms:
        tl = t.lower()
        if tl in title:
            score += 2.0
        if tl in body:
            score += 1.0
    return score


def _search_notes(notes: list[dict], query: str) -> list[dict]:
    """Filter and rank notes; attach snippet and title_html for rendering."""
    terms = [t for t in query.split() if t]
    if not terms:
        return notes

    results = []
    for note in notes:
        rank = _rank_note(note, terms)
        if rank > 0:
            snippet = _make_snippet(note.get("body") or "", terms)
            title_html = _highlight_terms(_html.escape(note.get("title") or ""), terms)
            results.append({**note, "snippet": snippet, "title_html": title_html, "_rank": rank})

    results.sort(key=lambda n: n["_rank"], reverse=True)
    for r in results:
        del r["_rank"]
    return results


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"
    app.config["DATABASE"] = "sandbox.db"
    if config:
        app.config.update(config)

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Each note carries a user_id field for per-user filtering.
    app.notes: list = []  # type: ignore[attr-defined]

    login_manager = LoginManager(app)
    login_manager.login_view = "login"  # type: ignore[assignment]

    @login_manager.user_loader
    def load_user(user_id: str):
        return find_by_id(app.config["DATABASE"], int(user_id))

    init_db(app.config["DATABASE"])

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                error = "Username and password are required"
            elif find_by_username(app.config["DATABASE"], username):
                error = "Username already taken"
            else:
                create_user(
                    app.config["DATABASE"],
                    username,
                    generate_password_hash(password),
                )
                return redirect(url_for("login"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = find_by_username(app.config["DATABASE"], username)
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("home"))
            error = "Invalid username or password"
        return render_template("login.html", error=error)

    @app.route("/logout", methods=["POST"])
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def home():
        user_notes = [
            n for n in app.notes
            if n.get("user_id") is None or n.get("user_id") == current_user.id
        ]
        q = request.args.get("q", "").strip()
        notes = _search_notes(user_notes, q) if q else user_notes
        return render_template("home.html", notes=notes, username=current_user.username, q=q)

    @app.route("/notes/new", methods=["GET", "POST"])
    @login_required
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            # TASK 01 will add validation here.
            app.notes.append({"title": title, "body": body, "user_id": current_user.id, "tags": []})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
