def average_rating(ratings):
    """Return the average of a list of ratings."""
    return sum(ratings) / len(ratings)

# Claude's test:
assert average_rating([4, 5, 3]) == 4.0


def fixed_average_rating(ratings):
    """Return the average of a list of ratings."""
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

# Claude's test:
assert average_rating([4, 5, 3]) == 4.0


def test_average_rating():
    assert average_rating([4, 5, 3]) == 4.0
    assert average_rating([]) == None  

def test_fixed_average_rating():
    assert fixed_average_rating([4, 5, 3]) == 4.0
    assert fixed_average_rating([]) == None  