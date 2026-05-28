def average_rating(ratings):
    """Return the average of a list of ratings."""
    if not ratings:
        return 0
    return sum(ratings) / len(ratings)
