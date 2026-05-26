from scratch import average_rating

def test_bughunt_03():
    r = average_rating([])
    print(r)
    assert "Cannot compute average of empty list" in str(r)


if __name__ == "__main__":
    test_bughunt_03()