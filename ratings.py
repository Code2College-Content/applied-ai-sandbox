def average_rating(ratings):
    """Return the average of a list of ratings."""
    return sum(ratings) / len(ratings) if ratings else 0.0
