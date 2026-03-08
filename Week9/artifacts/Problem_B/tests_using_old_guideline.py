# Example of typical LLM output when following Guideline 4 (Decompose) on clamp().
# This illustrates why the guideline does not work well for single-responsibility code.

import pytest
from clamp import clamp


# --- Step 1: LLM "identifies" behaviors (invented for a 3-line function) ---
# Behavior 1: "Handles value below lower bound"
# Behavior 2: "Handles value above upper bound"
# Behavior 3: "Handles value within range"
# Behavior 4: "Handles boundary values (value == lo, value == hi)"

# --- Step 2 & 3: Tests per "behavior" ---

class TestBehaviorBelowLowerBound:
    """Behavior: value < lo -> return lo."""

    def test_value_below_lo_returns_lo(self):
        assert clamp(-5.0, 0.0, 10.0) == 0.0

    def test_negative_value_below_lo(self):
        assert clamp(-100.0, -10.0, 10.0) == -10.0

    @pytest.mark.parametrize("value,lo,hi", [(-1, 0, 10), (0.5, 1.0, 2.0)])
    def test_boundary_below_lo(self, value, lo, hi):
        assert clamp(value, lo, hi) == lo


class TestBehaviorAboveUpperBound:
    """Behavior: value > hi -> return hi."""

    def test_value_above_hi_returns_hi(self):
        assert clamp(15.0, 0.0, 10.0) == 10.0

    def test_large_value_above_hi(self):
        assert clamp(1000.0, 0.0, 1.0) == 1.0

    @pytest.mark.parametrize("value,lo,hi", [(11, 0, 10), (2.5, 0.0, 2.0)])
    def test_boundary_above_hi(self, value, lo, hi):
        assert clamp(value, lo, hi) == hi


class TestBehaviorWithinRange:
    """Behavior: lo <= value <= hi -> return value."""

    def test_value_in_middle_unchanged(self):
        assert clamp(5.0, 0.0, 10.0) == 5.0

    def test_value_equals_midpoint(self):
        assert clamp(0.5, 0.0, 1.0) == 0.5


class TestBehaviorBoundaryEdges:
    """Behavior: value == lo or value == hi (boundary)."""

    def test_value_equals_lo_returns_lo(self):
        assert clamp(0.0, 0.0, 10.0) == 0.0

    def test_value_equals_hi_returns_hi(self):
        assert clamp(10.0, 0.0, 10.0) == 10.0


# --- Negative / exception path (invented; clamp() does not validate) ---
class TestBehaviorValidation:
    """LLM invents a "validation" behavior that the function does not have."""

    def test_none_value_raises(self):
        with pytest.raises(TypeError):
            clamp(None, 0.0, 10.0)  # May or may not raise; contract says "no validation"

    def test_lo_gt_hi_behavior(self):
        # Underspecified: contract says "assumes lo <= hi". LLM might assert anything.
        result = clamp(5.0, 10.0, 0.0)
        assert result in (0.0, 5.0, 10.0)  # Weak assertion

