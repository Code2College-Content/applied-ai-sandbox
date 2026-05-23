import pytest
from scratch import average_rating

def test_normal_list():
    assert average_rating([4, 5, 3]) == 4.0

def test_empty_list():
    assert average_rating([]) == 0.0