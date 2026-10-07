"""Unit tests for solution.monotonic().

Tests cover:
1. Normal cases with typical inputs (increasing, decreasing, non-monotonic).
2. Boundary cases at edges (single element, two elements, all equal).
3. Empty / zero-size inputs.
4. Edge cases with duplicates, negatives, zeros, large values.
5. Exception cases (invalid input types).
"""

import pytest
from solution import monotonic


# ──────────────────────────────────────────────
# 1. Normal cases – typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Typical increasing, decreasing, and non-monotonic lists."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_not_monotonic(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_three_elements_increasing(self):
        assert monotonic([1, 2, 3]) is True

    def test_three_elements_decreasing(self):
        assert monotonic([3, 2, 1]) is True

    def test_three_elements_not_monotonic(self):
        assert monotonic([1, 3, 2]) is False

    def test_longer_increasing_list(self):
        assert monotonic(list(range(100))) is True

    def test_longer_decreasing_list(self):
        assert monotonic(list(range(100, 0, -1))) is True


# ──────────────────────────────────────────────
# 2. Boundary cases – edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Edge-of-range inputs: single element, two elements, all-equal."""

    def test_single_element(self):
        # A single-element list is trivially monotonic
        assert monotonic([42]) is True

    def test_empty_list(self):
        # An empty list has no violating pair; both inc & dec stay True
        assert monotonic([]) is True

    def test_two_equal_elements(self):
        assert monotonic([5, 5]) is True

    def test_all_same_elements(self):
        assert monotonic([7, 7, 7, 7]) is True

    def test_all_zero(self):
        assert monotonic([0, 0, 0]) is True


# ──────────────────────────────────────────────
# 3. Duplicate handling (non-strict monotonicity)
# ──────────────────────────────────────────────

class TestDuplicates:
    """Lists with repeated values should still be monotonic when ordered."""

    def test_non_decreasing_with_duplicates(self):
        assert monotonic([1, 1, 2, 2, 3]) is True

    def test_non_increasing_with_duplicates(self):
        assert monotonic([5, 4, 4, 3, 3, 1]) is True

    def test_alternating_equal_pairs(self):
        assert monotonic([1, 1, 2, 2, 3, 3]) is True

    def test_dip_breaks_monotonicity(self):
        assert monotonic([1, 2, 2, 1]) is False

    def test_rise_after_flat_breaks_monotonicity(self):
        assert monotonic([3, 3, 4, 2]) is False


# ──────────────────────────────────────────────
# 4. Special numeric values
# ──────────────────────────────────────────────

class TestSpecialNumbers:
    """Negative numbers, zeros, floats, and large integers."""

    def test_negative_numbers_increasing(self):
        assert monotonic([-5, -3, -1, 0]) is True

    def test_negative_numbers_decreasing(self):
        assert monotonic([0, -1, -3, -5]) is True

    def test_mixed_positive_and_negative_increasing(self):
        assert monotonic([-10, -5, 0, 5, 10]) is True

    def test_mixed_positive_and_negative_decreasing(self):
        assert monotonic([10, 5, 0, -5, -10]) is True

    def test_floats_increasing(self):
        assert monotonic([1.1, 2.2, 3.3]) is True

    def test_floats_decreasing(self):
        assert monotonic([3.3, 2.2, 1.1]) is True

    def test_floats_not_monotonic(self):
        assert monotonic([1.0, 3.0, 2.0]) is False

    def test_large_integers_increasing(self):
        assert monotonic([10**15, 10**15 + 1, 10**15 + 2]) is True

    def test_large_integers_decreasing(self):
        assert monotonic([10**15, 10**15 - 1, 10**15 - 2]) is True

    def test_single_negative(self):
        assert monotonic([-42]) is True

    def test_single_zero(self):
        assert monotonic([0]) is True


# ──────────────────────────────────────────────
# 5. Invalid inputs – should raise exceptions
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Passing types that don't support __getitem__ / len will raise."""

    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            monotonic(None)

    def test_string_input_behavior(self):
        # Strings are indexable and comparable, so they won't raise.
        # "abc" is strictly increasing → True
        assert monotonic("abc") is True

    def test_integer_input_raises(self):
        with pytest.raises(TypeError):
            monotonic(42)

    def test_dict_input_returns_true(self):
        # A dict with a single key has len==1, so the loop body never runs.
        # Both inc and dec remain True → returns True.
        assert monotonic({"a": 1}) is True

    def test_set_input_raises(self):
        # Sets are not subscriptable; l[i] raises TypeError inside the function.
        with pytest.raises(TypeError):
            monotonic({1, 2, 3})

    def test_tuple_input(self):
        # Tuples are indexable, so they work fine.
        assert monotonic((1, 2, 3)) is True

    def test_frozenset_input_raises(self):
        # Frozensets are also not subscriptable.
        with pytest.raises(TypeError):
            monotonic(frozenset({1, 2, 3}))


# ──────────────────────────────────────────────
# 6. Docstring doctests (re-run via pytest)
# ──────────────────────────────────────────────

def test_doctest_examples():
    """Reproduce the three examples from the docstring."""
    assert monotonic([1, 2, 4, 20]) is True
    assert monotonic([1, 20, 4, 10]) is False
    assert monotonic([4, 1, 0, -10]) is True
