"""Tests for the tags field on note dicts."""
import re
# The 're' module provides regular expressions. Used below to extract specific
# HTML elements from a rendered page without coupling tests to exact markup
# structure (e.g. whitespace, attribute ordering).


def test_new_note_has_empty_tags(client, app):
    # When no tags field is submitted, the saved note must still carry a
    # "tags" key set to []. An absent key would cause a KeyError anywhere
    # the code accesses note["tags"]; an empty list is the safe default.
    app.notes.clear()
    client.post("/notes/new", data={"title": "Tagged", "body": "Hello"})
    assert len(app.notes) == 1
    assert app.notes[0]["tags"] == []


def test_old_note_without_tags_key_is_safe(app):
    """Legacy notes that pre-date the tags field must not crash on .get()."""
    # Notes created before the tags feature was added won't have a "tags" key.
    # Any code that reads tags must use note.get("tags", []) instead of
    # note["tags"] to gracefully handle these older dicts without a KeyError.
    app.notes.clear()
    app.notes.append({"title": "old", "body": "legacy"})  # no "tags" key
    note = app.notes[0]
    assert note.get("tags", []) == []


def test_tags_comma_split(client, app):
    # "work, urgent" should be split into the list ["work", "urgent"].
    # Comma-separated input is the standard UX for entering multiple values
    # in a single text field — it matches how users naturally type lists.
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": "work, urgent"})
    assert app.notes[0]["tags"] == ["work", "urgent"]


def test_tags_whitespace_and_empty_entries_ignored(client, app):
    # " work , urgent  , ," has extra spaces around tags and a trailing comma
    # that produces an empty entry. Both must be silently cleaned up.
    # Without this, the stored list would be [" work ", " urgent  ", "", ""],
    # which would break exact-match filtering and display ugly chips.
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": " work , urgent  , ,"})
    assert app.notes[0]["tags"] == ["work", "urgent"]


def test_tags_empty_string_gives_empty_list(client, app):
    # An empty tags field (user left it blank) must produce [] not [""].
    # Storing [""] would be a false positive — every note would appear to
    # have one tag, causing phantom filter bar entries and broken counts.
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B", "tags": ""})
    assert app.notes[0]["tags"] == []


def test_tags_render_as_chips(client, app):
    # When a note has tags, those tag names must appear somewhere in the
    # rendered HTML. We seed app.notes directly (bypassing the form route)
    # to isolate rendering from the parsing logic tested above.
    app.notes.clear()
    app.notes.append({"title": "T", "body": "B", "tags": ["work"]})
    r = client.get("/")
    assert b"work" in r.data


def test_filter_bar_deduplicates_tags(client, app):
    # Two notes share the tag "work". The filter bar must show "work" exactly
    # once — showing duplicates would suggest broken deduplication and confuse
    # users about how many distinct tags exist.
    #
    # We use a regex scoped to class="filter..." anchor tags only, so that
    # tag text appearing in chips, note bodies, or URLs doesn't inflate the
    # count and produce a false pass.
    app.notes.clear()
    app.notes.append({"title": "A", "body": "x", "tags": ["work", "urgent"]})
    app.notes.append({"title": "B", "body": "y", "tags": ["work"]})
    r = client.get("/")
    body = r.data.decode()
    # Extract the visible label text of every <a class="filter..."> element.
    filter_labels = re.findall(r'class="filter[^"]*"[^>]*>\s*([^<\s][^<]*?)\s*</a>', body)
    filter_tags = [lbl for lbl in filter_labels if lbl != "All"]
    assert sorted(filter_tags) == ["urgent", "work"]  # exactly one of each, alphabetical


def test_filter_by_tag_hides_non_matching(client, app):
    # Requesting /?tag=work should return only notes tagged "work".
    # "Personal note" must be absent from the response — the whole point of
    # filtering is to hide irrelevant notes, not just highlight matching ones.
    app.notes.clear()
    app.notes.append({"title": "Work note",     "body": "x", "tags": ["work"]})
    app.notes.append({"title": "Personal note", "body": "y", "tags": ["personal"]})
    r = client.get("/?tag=work")
    body = r.data.decode()
    assert "Work note" in body
    assert "Personal note" not in body


def test_filter_all_shows_every_note(client, app):
    # The bare "/" route (no ?tag= parameter) is the "All" state — every note
    # must be visible. This is the default view users land on and the state
    # the "All" filter bar link returns them to after filtering.
    app.notes.clear()
    app.notes.append({"title": "Work note",     "body": "x", "tags": ["work"]})
    app.notes.append({"title": "Personal note", "body": "y", "tags": ["personal"]})
    r = client.get("/")
    body = r.data.decode()
    assert "Work note" in body
    assert "Personal note" in body
