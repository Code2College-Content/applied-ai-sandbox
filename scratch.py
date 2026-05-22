def average_rating(ratings):
    """Return the average of a list of ratings."""
    return sum(ratings) / len(ratings)

# Claude's test:
assert average_rating([4, 5, 3]) == 4.0