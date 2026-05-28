def average_rating(ratings):
    if not ratings:
        return 0

    return sum(ratings) / len(ratings)