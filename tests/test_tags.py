from app import parse_tags


def test_empty_string():
    assert parse_tags("") == []


def test_strips_and_drops_empty():
    assert parse_tags("work, urgent , ") == ["work", "urgent"]


def test_single_tag_with_spaces():
    assert parse_tags("  personal  ") == ["personal"]
