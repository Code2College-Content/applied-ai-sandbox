# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+
- Flask 3.x (no SQLAlchemy, no Flask-Login — intentionally minimal)
- pytest
- Jinja2 templates, vanilla HTML/CSS (no base template — each page has inline styles)

## How to run things

```bash
# Activate the virtual environment (Windows PowerShell)
.venv\Scripts\activate

# Run the app
python app.py
# → http://localhost:5000

# Run all tests
pytest

# Run tests for a single task
pytest tests/test_task_01.py
```

## Architecture

**Single-file app with a factory function.** `app.py` exports `create_app()` — all routes and helpers are defined inside it. There is no `models.py` or database.

**In-memory state lives on the `app` object:**
- `app.notes` — `list[dict]` where each dict has `"title"` and `"body"` keys
- `app.users` — `dict[str, str]` mapping username → werkzeug-hashed password

Both reset on every restart; that's intentional for this sandbox.

**Auth** is a hand-rolled `login_required` decorator (defined inside `create_app`) that checks `session["username"]`. Passwords are hashed with `werkzeug.security.generate_password_hash` / `check_password_hash`. There is no Flask-Login.

## Test fixtures (`tests/conftest.py`)

- `app` fixture — creates a fresh `create_app()` instance with `TESTING=True`
- `client` fixture — wraps `app.test_client()` and **pre-registers + logs in** as `testuser`/`testpass` via `/register`

This means every test using `client` is already authenticated. Tests that seed notes should call `app.notes.clear()` first to ensure a clean state.

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/` instead.
- Keep changes scoped to the task. Don't refactor unrelated files.
- When unsure, prefer reading the test file first — it tells you exactly what behavior is expected.

## Working with Claude here

- Always read the task file (`tasks/TASK_NN.md`) and its test file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The tests are the spec.
