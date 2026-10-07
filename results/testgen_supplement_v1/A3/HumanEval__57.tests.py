"""Unit tests for solution.monotonic().

The monotonic function returns True if list elements are monotonically
increasing (non-decreasing) or monotonically decreasing (non-increasing),
and False otherwise.
"""

import pytest
from solution import monotonic


# ── Normal / typical cases ────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical non-trivial inputs."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_not_monotonic(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_non_decreasing_with_duplicates(self):
        assert monotonic([1, 2, 2, 3]) is True

    def test_non_increasing_with_duplicates(self):
        assert monotonic([5, 3, 3, 1]) is True

    def test_all_equal(self):
        assert monotonic([7, 7, 7, 7]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_negative_numbers_increasing(self):
        assert monotonic([-5, -3, -1, 0]) is True

    def test_negative_numbers_decreasing(self):
        assert monotonic([0, -1, -3, -5]) is True

    def test_mixed_positive_negative_increasing(self):
        assert monotonic([-10, -5, 0, 5, 10]) is True

    def test_single_peak_not_monotonic(self):
        assert monotonic([1, 3, 2]) is False

    def test_single_valley_not_monotonic(self):
        assert monotonic([3, 1, 3]) is False


# ── Boundary cases ────────────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_empty_list(self):
        """An empty list is trivially monotonic (no pairs to violate order)."""
        assert monotonic([]) is True

    def test_single_element(self):
        """A single-element list is trivially monotonic."""
        assert monotonic([42]) is True

    def test_two_equal_elements(self):
        assert monotonic([5, 5]) is True

    def test_large_values(self):
        assert monotonic([0, 10**18, 2 * 10**18]) is True

    def test_large_negative_values(self):
        assert monotonic([-2 * 10**18, -10**18, 0]) is True

    def test_float_increasing(self):
        assert monotonic([0.1, 0.2, 0.3, 0.4]) is True

    def test_float_decreasing(self):
        assert monotonic([0.4, 0.3, 0.2, 0.1]) is True

    def test_float_with_duplicates(self):
        assert monotonic([1.0, 1.0, 2.0]) is True

    def test_zero_and_negative(self):
        assert monotonic([0, -1, -2, -3]) is True

    def test_long_constant_sequence(self):
        assert monotonic([0] * 1000) is True

    def test_long_increasing_sequence(self):
        assert monotonic(list(range(1000))) is True

    def test_long_decreasing_sequence(self):
        assert monotonic(list(range(999, -1, -1))) is True


# ── Invalid / edge-case inputs ────────────────────────────────────────

class TestEdgeCaseInputs:
    """Tests for unusual but plausible inputs."""

    def test_list_with_one_change_point(self):
        """Exactly one ascent then descent — not monotonic."""
        assert monotonic([1, 2, 3, 2, 1]) is False

    def test_list_with_one_descent_then_ascent(self):
        assert monotonic([3, 2, 1, 2, 3]) is False

    def test_alternating_up_down(self):
        assert monotonic([1, 3, 2, 4, 3, 5]) is False

    def test_all_zeros(self):
        assert monotonic([0, 0, 0, 0, 0]) is True

    def test_very_long_flat_list(self):
        assert monotonic([1] * 10000) is True


# ── Docstring examples (doctest-style verification) ──────────────────

class TestDocstringExamples:
    """Verify the examples from the docstring produce expected results."""

    def test_docstring_example_1(self):
        # >>> monotonic([1, 2, 4, 20])
        assert monotonic([1, 2, 4, 20]) is True

    def test_docstring_example_2(self):
        # >>> monotonic([1, 20, 4, 10])
        assert monotonic([1, 20, 4, 10]) is False

    def test_docstring_example_3(self):
        # >>> monotonic([4, 1, 0, -10])
        assert monotonic([4, 1, 0, -10]) is True
