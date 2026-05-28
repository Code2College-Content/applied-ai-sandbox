
from __future__ import annotations

import unicodedata
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request, redirect, url_for


def parse_tags(raw: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for tag in raw.split(","):
        tag = tag.strip().lower()
        if tag and tag not in seen:
            seen.add(tag)
            result.append(tag)
    return result


def _normalize(s: str) -> str:
    return unicodedata.normalize("NFC", s).lower()


def _make_snippet(body: str, query: str, max_len: int = 160) -> str:
    idx = _normalize(body).find(_normalize(query))
    if idx == -1:
        return body[:max_len]
    half = max_len // 2
    start = max(0, idx - half)
    end = min(len(body), start + max_len)
    return ("…" if start else "") + body[start:end] + ("…" if end < len(body) else "")


def _search_notes(notes: list[dict], query: str) -> list[dict]:
    search_string = _normalize(query)
    results = []
    for note in notes:
        in_title = search_string in _normalize(note["title"])
        in_body = search_string in _normalize(note.get("body") or "")
        if not (in_title or in_body):
            continue
        matched_in = "both" if (in_title and in_body) else ("title" if in_title else "body")
        snippet = _make_snippet(note.get("body") or "", query) if in_body else None
        results.append({**note, "matched_in": matched_in, "snippet": snippet})
    results.sort(key=lambda r: 0 if r["matched_in"] in ("title", "both") else 1)
    return results


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        # Older in-memory notes (or tests) might not have created_at yet.
        for note in app.notes:
            if "created_at" not in note:
                note["created_at"] = None
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            if not title:
                return render_template("new_note.html", error="Title is required", title=title, body=body)
            if not body:
                return render_template("new_note.html", error="Body is required", title=title, body=body)
            tags = parse_tags(request.form.get("tags") or "")
            created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            app.notes.append({"title": title, "body": body, "tags": tags, "created_at": created_at})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes")
    def list_notes():
        query = (request.args.get("q") or "").strip()
        if len(query) > 200:
            return jsonify({"error": "Query too long (max 200 characters)"}), 400

        try:
            page = max(1, int(request.args.get("page", 1)))
            limit = min(100, max(1, int(request.args.get("limit", 20))))
        except ValueError:
            return jsonify({"error": "page and limit must be integers"}), 400

        for note in app.notes:
            note.setdefault("created_at", None)

        if query:
            matched = _search_notes(app.notes, query)
        else:
            matched = [{**note, "matched_in": None, "snippet": None} for note in app.notes]

        total = len(matched)
        start = (page - 1) * limit
        page_notes = matched[start: start + limit]

        return jsonify({"notes": page_notes, "total_count": total, "query": query})

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
