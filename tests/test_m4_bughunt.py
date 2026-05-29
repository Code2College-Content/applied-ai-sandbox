from scratch import average_rating


def test_average_rating_empty_list_returns_zero():
    assert average_rating([]) == 0


def test_average_rating_normal_case():
    assert average_rating([4, 5, 3]) == 4.0
