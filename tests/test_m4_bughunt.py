from ratings import average_rating


def test_average_rating_handles_empty_list():
    assert average_rating([]) == 0
