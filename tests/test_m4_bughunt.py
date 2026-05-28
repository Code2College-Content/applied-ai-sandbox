def average_rating(ratings):
    if not ratings:
        return 0

    return sum(ratings) / len(ratings)

def test_average_rating_empty_list():
    assert average_rating([]) == 0