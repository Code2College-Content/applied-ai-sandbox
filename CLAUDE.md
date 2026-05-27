# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+
- Flask 3.x
- pytest
- Jinja2 templates, vanilla HTML/CSS

## Architecture

**App factory**
`app.py` exposes `create_app() -> Flask`. Tests call this to get a fresh, isolated instance per test. The bottom of `app.py` also calls it for `python app.py` dev use.

**In-memory data store**
Notes live on `app.notes` — a plain Python list of `{"title": str, "body": str}` dicts. No database; the list resets on every restart (intentional for sandbox simplicity).

**Routes**
- `GET /` → `home.html` — lists all notes
- `GET/POST /notes/new` → `new_note.html` — create form; POST validates, persists, and redirects on success
- *(TASK 02 adds)* `POST /notes/<idx>/delete` — removes note by list index, redirects

**Template conventions**
Forms preserve user input on re-render via `{{ value or '' }}`. Validation error messages are displayed in `new_note.html` when a POST fails.

**Test fixtures (`tests/conftest.py`)**
- `app` — `create_app({"TESTING": True})` with a clean `app.notes = []` each test
- `client` — `app.test_client()` for making HTTP requests

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

## Working with Claude here

- Always read the task file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The
  tests are the spec.
