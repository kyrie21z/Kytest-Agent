"""Unit tests for generate_integers."""

import pytest
from solution import generate_integers


# ── Normal / typical cases ──────────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical valid inputs from the docstring and common scenarios."""

    def test_example_1(self):
        """Docstring example: generate_integers(2, 8) => [2, 4, 6, 8]"""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_example_2_swapped(self):
        """Docstring example: generate_integers(8, 2) => [2, 4, 6, 8]"""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_example_3_no_even_digits(self):
        """Docstring example: generate_integers(10, 14) => []"""
        assert generate_integers(10, 14) == []

    def test_range_1_to_9(self):
        """Full span of single-digit positives yields all four evens."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_partial_range(self):
        """Range 3..7 includes only 4 and 6."""
        assert generate_integers(3, 7) == [4, 6]

    def test_reversed_partial_range(self):
        """Same partial range given in reverse order."""
        assert generate_integers(7, 3) == [4, 6]

    def test_single_even_number(self):
        """Range containing exactly one even number."""
        assert generate_integers(2, 2) == [2]

    def test_single_odd_number(self):
        """Range containing exactly one odd number."""
        assert generate_integers(3, 3) == []

    def test_two_consecutive_evens(self):
        """Range 4..6 includes 4 and 6."""
        assert generate_integers(4, 6) == [4, 6]

    def test_two_consecutive_odds(self):
        """Range 3..5 includes only 4."""
        assert generate_integers(3, 5) == [4]

    def test_large_b_capped_at_10(self):
        """When b is large, the effective upper bound is 10."""
        assert generate_integers(2, 100) == [2, 4, 6, 8]

    def test_large_a_and_b_above_9(self):
        """Both arguments above 9 yield an empty list."""
        assert generate_integers(100, 200) == []

    def test_large_swapped_above_9(self):
        """Swapped large arguments still yield empty."""
        assert generate_integers(200, 100) == []

    def test_a_equals_b_even(self):
        """a == b where both are even."""
        assert generate_integers(6, 6) == [6]

    def test_a_equals_b_odd(self):
        """a == b where both are odd."""
        assert generate_integers(7, 7) == []


# ── Boundary cases ──────────────────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of the valid input range."""

    def test_min_positive_a(self):
        """Smallest positive integer as lower bound."""
        assert generate_integers(1, 8) == [2, 4, 6, 8]

    def test_max_single_digit_b(self):
        """Upper bound exactly at 9 (last single digit)."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_upper_bound_exactly_10(self):
        """Upper bound at 10 — still capped, no new evens added."""
        assert generate_integers(1, 10) == [2, 4, 6, 8]

    def test_lower_bound_at_8(self):
        """Lower bound at 8, upper bound beyond."""
        assert generate_integers(8, 20) == [8]

    def test_lower_bound_at_9(self):
        """Lower bound at 9 (odd), upper bound beyond."""
        assert generate_integers(9, 20) == []

    def test_upper_bound_at_1(self):
        """Upper bound at 1 — no even digits possible."""
        assert generate_integers(1, 1) == []

    def test_both_bounds_at_10(self):
        """Both bounds at 10 — range is empty."""
        assert generate_integers(10, 10) == []

    def test_one_below_nine_one_above(self):
        """One argument below 10, one above — only evens below 10 included."""
        assert generate_integers(5, 15) == [6, 8]


# ── Edge cases: empty / zero-size inputs ────────────────────────────────────

class TestEmptyZeroSize:
    """Tests where the result is expected to be empty."""

    def test_zero_as_input(self):
        """Zero is not a positive integer per doc, but function handles it."""
        # range(0, 10) with even filter → [0, 2, 4, 6, 8]
        # However, doc says "positive integers". We test actual behavior.
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_negative_a(self):
        """Negative a gets swapped; effective range starts from negative."""
        # range(-5, 10) with even filter → [-4, -2, 0, 2, 4, 6, 8]
        assert generate_integers(-5, 9) == [-4, -2, 0, 2, 4, 6, 8]

    def test_both_negative(self):
        """Both negative — even negatives in range."""
        # range(-10, -5) → [-10, -9, -8, -7, -6], evens → [-10, -8, -6]
        assert generate_integers(-10, -5) == [-10, -8, -6]

    def test_range_with_only_zeros(self):
        """Range covering just 0."""
        assert generate_integers(0, 0) == [0]


# ── Exception / invalid input cases ─────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs outside documented constraints."""

    def test_non_integer_float(self):
        """Float inputs — Python's range() will raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers(2.5, 8)

    def test_string_input(self):
        """String inputs — range() will raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers("2", "8")

    def test_none_input(self):
        """None input — range() will raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers(None, 8)

    def test_mixed_types(self):
        """Mixing int and str raises TypeError."""
        with pytest.raises(TypeError):
            generate_integers(2, "8")

    def test_empty_list_input(self):
        """List input instead of int raises TypeError."""
        with pytest.raises(TypeError):
            generate_integers([], [])
