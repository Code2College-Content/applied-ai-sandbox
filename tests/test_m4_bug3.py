from scratch import average_rating

def test_empty_list_returns_zero():
    assert average_rating([]) == 0

def test_single_rating():
    assert average_rating([5]) == 5.0

def test_multiple_ratings():
    assert average_rating([4, 5, 3]) == 4.0

def test_all_same_ratings():
    assert average_rating([3, 3, 3]) == 3.0
