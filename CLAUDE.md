# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+, Flask 3.x, pytest, Jinja2 templates, vanilla HTML/CSS
- `pyproject.toml` sets `pythonpath = ["."]` so pytest can import `app.py` from the repo root

## How to run things

```bash
python app.py                       # → http://localhost:5000
pytest                              # run all tests
pytest tests/test_task_01.py        # run a single task's tests
```

## Data model

`app.notes` is a plain Python list (reset on restart) of dicts:

```python
{"title": str, "body": str}
```

Notes are appended on `POST /notes/new` and accessed by list index everywhere.

## Key patterns

- **Post-Redirect-Get**: successful form submissions redirect to `/`; validation failures re-render the form with a 200.
- **Value preservation**: templates use `{{ title or '' }}` / `{{ body or '' }}` so user-typed values survive a failed submit.
- **Error display**: `new_note.html` has an `.error` CSS class and a comment marking where TASK_01 should surface messages.
- **Delete route**: uses `methods=["POST"]` only; Flask returns 405 automatically for GET. Index lookup is wrapped in `try/except IndexError` → `abort(404)`.

## Test structure

`tests/conftest.py` provides two fixtures used by every test file:
- `app` — creates the Flask app with `TESTING=True`
- `client` — returns a Flask test client

Tests that need pre-seeded notes set them directly on `app.notes` before making requests.

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/` instead.
- Keep changes scoped to the task. Don't refactor unrelated files.
- When unsure, prefer reading the test file first — it tells you exactly what behavior is expected.

## Working with Claude here

- Always read the task file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The tests are the spec.
