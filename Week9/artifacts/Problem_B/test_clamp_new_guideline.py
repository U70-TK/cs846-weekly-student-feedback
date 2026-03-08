import pytest
from Week9.artifacts.problem_b.clamp import clamp

# Behavior 1: Value below lower bound
@pytest.mark.parametrize("value, lo, hi, expected", [
    (0, 1, 5, 1),
    (-10, -5, 0, -5),
    (-100, -50, -10, -50),
])
def test_clamp_value_below_lo(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected

# Behavior 2: Value above upper bound
@pytest.mark.parametrize("value, lo, hi, expected", [
    (10, 1, 5, 5),
    (1, -5, 0, 0),
    (100, -50, -10, -10),
])
def test_clamp_value_above_hi(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected

# Behavior 3: Value within bounds (including at boundaries)
@pytest.mark.parametrize("value, lo, hi, expected", [
    (3, 1, 5, 3),
    (1, 1, 5, 1),  # at lower bound
    (5, 1, 5, 5),  # at upper bound
    (-5, -5, 0, -5),  # at lower bound
    (0, -5, 0, 0),  # at upper bound
    (-10, -50, -10, -10),  # at upper bound
    (-50, -50, -10, -50),  # at lower bound
])
def test_clamp_value_within_bounds(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected

# Behavior 4: No validation for lo > hi (assumes lo <= hi)
def test_clamp_no_validation_lo_gt_hi():
    # Function does not validate lo > hi, so result may be unexpected
    assert clamp(5, 10, 1) == 10  # value < lo, returns lo
    assert clamp(-5, 10, 1) == 10  # value < lo, returns lo
    assert clamp(15, 10, 1) == 10  # value > hi, returns lo

# Behavior 5: Handling of float values and precision
@pytest.mark.parametrize("value, lo, hi, expected", [
    (1.5, 1.0, 2.0, 1.5),
    (0.999999, 1.0, 2.0, 1.0),
    (2.000001, 1.0, 2.0, 2.0),
    (1.0, 1.0, 2.0, 1.0),
    (2.0, 1.0, 2.0, 2.0),
])
def test_clamp_float_precision(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected

# Behavior 6: Negative cases (invalid types)
@pytest.mark.parametrize("value, lo, hi", [
    (None, 1, 5),
    (3, None, 5),
    (3, 1, None),
    ("a", 1, 5),
    (3, "b", 5),
    (3, 1, "c"),
])
def test_clamp_invalid_types(value, lo, hi):
    with pytest.raises(TypeError):
        clamp(value, lo, hi)
