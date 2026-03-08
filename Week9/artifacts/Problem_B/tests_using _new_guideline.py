# Example of tests following the NEW guideline (match structure to complexity).
# Single-responsibility function -> one focused suite, boundary + fault-model.

import pytest
from clamp import clamp


# --- Boundary cases (strong assertions, exact expected values) ---

@pytest.mark.parametrize("value,lo,hi,expected", [
    (-1.0, 0.0, 10.0, 0.0),
    (-100.0, -10.0, 10.0, -10.0),
])
def test_below_lo_returns_lo(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected


@pytest.mark.parametrize("value,lo,hi,expected", [
    (11.0, 0.0, 10.0, 10.0),
    (100.0, 0.0, 1.0, 1.0),
])
def test_above_hi_returns_hi(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected


@pytest.mark.parametrize("value,lo,hi", [
    (5.0, 0.0, 10.0),
    (0.0, 0.0, 10.0),   # boundary: value == lo
    (10.0, 0.0, 10.0),  # boundary: value == hi
])
def test_in_range_returns_value(value, lo, hi):
    assert clamp(value, lo, hi) == value


# --- Fault model: tests that would FAIL if the bug exists ---

# FM1: Lower bound uses <= instead of < (value == lo would wrongly return lo)
def test_fm1_lower_bound_strict_inequality():
    # value == lo must still return value (lo); if impl used <= for "clamp low", might be wrong
    assert clamp(0.0, 0.0, 10.0) == 0.0  # targets: FM1


# FM2: Upper bound uses < instead of > (value == hi would not return hi)
def test_fm2_upper_bound_strict_inequality():
    assert clamp(10.0, 0.0, 10.0) == 10.0  # targets: FM2


# FM3: Forgets to clamp low (returns value when value < lo)
def test_fm3_below_lo_returns_lo_not_value():
    assert clamp(-5.0, 0.0, 10.0) == 0.0  # targets: FM3
