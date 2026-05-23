# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

Python 3.10+, Flask 3.x, pytest, Jinja2 templates, vanilla HTML/CSS.

## Commands

```bash
python app.py                       # Run the app → http://localhost:5000
pytest                              # Run all tests
pytest tests/test_task_01.py        # Run tests for a single task
```

## Architecture

`app.py` exports a `create_app()` factory that registers all routes and
returns the Flask instance. The in-memory note store lives at
`app.notes: list[dict]` where each dict has `"title"` and `"body"` string
keys. It resets on every restart — intentionally, no database.

**Tests** (`tests/conftest.py`) call `create_app()` directly and expose
two pytest fixtures used across all test files:
- `app` — fresh app instance with `TESTING=True`
- `client` — Flask test client bound to that app instance

**Templates** receive these variables:
- `home.html` → `notes` (the full list from `app.notes`)
- `new_note.html` → `title`, `body` (preserved form values on validation
  failure) and error message variables to surface inline errors

`pyproject.toml` sets `pythonpath = ["."]` so bare `pytest` can import
`app.py` from the repo root without `python -m pytest`.

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is
  "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/`
  instead.
- Keep changes scoped to the task. Don't refactor unrelated files.
- Always read the task file and the corresponding test file before writing
  code — the tests are the spec.
- Run `pytest` after each substantive change.
