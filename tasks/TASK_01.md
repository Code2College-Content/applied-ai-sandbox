# Task 01 — Validate the new-note form

## Goal
Right now the "New note" form happily accepts an empty title or body —
which means the homepage shows a list of empty bullet points after a
careless click. Add server-side validation so empty notes can't be
submitted, and surface a friendly error to the user.

## Acceptance criteria
- Submitting the form with an empty `title` re-renders `new_note.html`
  with an error message containing the text **"Title is required"**.
- Submitting with an empty `body` re-renders with an error message
  containing **"Body is required"**.
- When validation fails, the user's already-typed values stay populated
  in the form (no losing their work).
- A successful submit (both fields non-empty) still adds the note and
  redirects to `/`.
- All tests in `tests/test_task_01.py` pass.

## Files you'll likely touch
- `app.py` — the `new_note` view
- `templates/new_note.html` — render error messages

## Suggested workflow with Claude
1. `Read tasks/TASK_01.md and tests/test_task_01.py. Then propose a plan to make the tests pass without editing the test file.`
2. Review the plan. Push back on anything that doesn't match the criteria.
3. `Implement the plan. Run pytest tests/test_task_01.py after each file change.`
4. Once green, run all tests: `pytest`.

## What you should NOT do
- Don't edit `tests/test_task_01.py` to make it pass.
- Don't add a database — the in-memory list is fine.
- Don't refactor unrelated code.

Done...?
