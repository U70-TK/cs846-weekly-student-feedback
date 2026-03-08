import pytest
from clamp import clamp

@pytest.mark.parametrize("value, lo, hi, expected", [
    # value below lo
    (-1, 0, 10, 0),
    (-100, -50, -10, -50),
    (4.9, 5, 10, 5),
    # value above hi
    (11, 0, 10, 10),
    (0, -50, -10, -10),
    (10.1, 5, 10, 10),
    # value in range
    (5, 0, 10, 5),
    (-20, -50, -10, -20),
    (7.5, 5, 10, 7.5),
    # value == lo
    (0, 0, 10, 0),
    (-50, -50, -10, -50),
    (5, 5, 10, 5),
    # value == hi
    (10, 0, 10, 10),
    (-10, -50, -10, -10),
    (10, 5, 10, 10),
])
def test_clamp_contract(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected

# Fault Model FM1: Lower bound uses <= instead of <
def test_clamp_lower_bound_strict():
    # If bug exists, value == lo would return lo+1 or not lo
    assert clamp(0, 0, 10) == 0
    assert clamp(-50, -50, -10) == -50
    assert clamp(5, 5, 10) == 5

# Fault Model FM2: Upper bound uses < instead of >
def test_clamp_upper_bound_strict():
    # If bug exists, value == hi would return hi-1 or not hi
    assert clamp(10, 0, 10) == 10
    assert clamp(-10, -50, -10) == -10
    assert clamp(10, 5, 10) == 10

# Fault Model FM3: Returns value when value < lo (forgets to clamp low)
@pytest.mark.parametrize("value, lo, hi", [
    (-1, 0, 10),
    (-100, -50, -10),
    (4.9, 5, 10),
])
def test_clamp_clamps_low(value, lo, hi):
    assert clamp(value, lo, hi) == lo
