app.py
Locate the new_note view function.
Read title and body from request.form.
Call .strip() on both values so whitespace-only input counts as empty.
Create an errors list.
Add validation:
if title is empty → append "Title is required"
if body is empty → append "Body is required"
If errors is not empty:
return render_template("new_note.html", ...)
pass:
errors
title
body
Keep the existing successful-submit behavior:
append the note
redirect to /
templates/new_note.html
Add a section near the top of the form to display validation errors.
Loop through the errors list and render each message.

Update the title input so it preserves the submitted value:

value="{{ title or '' }}"

Update the body textarea so it preserves submitted content:

{{ body or '' }}
Do not remove or change the form field names (title, body).
Validation behavior to verify
Empty title:
page re-renders
contains "Title is required"
Empty body:
page re-renders
contains "Body is required"
Failed submit:
previously typed values remain in the form
Successful submit:
note still gets added
redirect to /
Test commands

Run task-specific tests first:

pytest tests/test_task_01.py

Then run the full suite:

pytest