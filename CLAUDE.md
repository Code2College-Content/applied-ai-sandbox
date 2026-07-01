# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Context Claude Code reads automatically when started in this repo.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+
- Flask 3.x
- pytest
- Jinja2 templates, vanilla HTML/CSS

## How to run things

```bash
# Run the app
python app.py
# → http://localhost:5000

# Run all tests
pytest

# Run tests for a single task
pytest tests/test_task_01.py
```

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is
  "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/`
  instead.
- Keep changes scoped to the task. Don't refactor unrelated files.
- When unsure, prefer reading the test file first — it tells you exactly
  what behavior is expected.

## Architecture

`app.py` uses a `create_app()` factory that initializes Flask, attaches `app.notes`, and registers all routes. There are no blueprints, no ORM, and no database.

**Data model:** `app.notes` is a plain Python list of `{"title": str, "body": str}` dicts. Notes are indexed by list position. The list resets on every restart — this is intentional.

**Routes:**

| Method | Path | View | Behavior |
|--------|------|------|----------|
| GET | `/` | `home` | renders `home.html` with all notes |
| GET/POST | `/notes/new` | `new_note` | GET shows form; POST validates and saves |
| POST | `/notes/<idx>/delete` | `delete_note` | removes note at index; 405 on GET; 404 on bad index |

**Form handling pattern:**
1. `request.form.get(field, "").strip()` to clean inputs
2. Validate — collect errors
3. On failure: re-render the same template with status 200 and preserved field values
4. On success: `redirect(url_for("home"))` → 302/303

**Testing setup:** `tests/conftest.py` provides `app` (Flask instance with `TESTING=True`) and `client` (test client) fixtures. Tests assert on `r.status_code` and byte strings in `r.data`. Side effects are verified via `app.notes` directly. `test_task_02.py` includes a `_seed(app, n)` helper to prepopulate notes.

## Working with Claude here

- Always read the task file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The
  tests are the spec.

## Auth
- Use Flask-Login + werkzeug.security for password hashing.
- Never roll a custom auth flow; never store plaintext passwords.
- Password reset / email verification are out of scope for now.