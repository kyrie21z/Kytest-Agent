"""Unit tests for generate_integers."""

import pytest
from solution import generate_integers


class TestGenerateIntegers_NormalCases:
    """Tests with typical, expected inputs."""

    def test_basic_range(self):
        """Even digits from 2 to 8."""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_reversed_order(self):
        """Inputs given as (larger, smaller) should be swapped."""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_no_even_digits_in_range(self):
        """Range 10 to 14 has no single-digit numbers."""
        assert generate_integers(10, 14) == []

    def test_full_digit_range(self):
        """All even digits from 1 to 9."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_single_even_digit(self):
        """Range contains exactly one even number."""
        assert generate_integers(2, 2) == [2]

    def test_single_odd_digit(self):
        """Range contains exactly one odd number — no evens."""
        assert generate_integers(3, 3) == []

    def test_mixed_range(self):
        """Range 3 to 7 contains 4 and 6."""
        assert generate_integers(3, 7) == [4, 6]

    def test_large_b_capped_at_10(self):
        """When b >= 9, the effective upper bound is 10 (exclusive)."""
        assert generate_integers(1, 100) == [2, 4, 6, 8]

    def test_large_b_capped_at_10_with_a_gt_1(self):
        """Large b still capped; a filters out small numbers."""
        assert generate_integers(5, 999) == [6, 8]

    def test_equal_inputs_both_even(self):
        """Both inputs equal and even."""
        assert generate_integers(6, 6) == [6]

    def test_equal_inputs_both_odd(self):
        """Both inputs equal and odd."""
        assert generate_integers(7, 7) == []


class TestGenerateIntegers_BoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_zero_lower_bound(self):
        """Lower bound is 0 (smallest non-negative digit)."""
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_zero_both_bounds(self):
        """Both bounds are 0."""
        assert generate_integers(0, 0) == [0]

    def test_upper_bound_exactly_9(self):
        """Upper bound is exactly 9 (last single-digit number)."""
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_upper_bound_is_10(self):
        """Upper bound is 10 — min(b+1, 10) = 10, so range stops before 10."""
        assert generate_integers(0, 10) == [0, 2, 4, 6, 8]

    def test_a_equals_b_equals_9(self):
        """Both bounds are 9 (odd, last digit)."""
        assert generate_integers(9, 9) == []

    def test_a_equals_b_equals_8(self):
        """Both bounds are 8 (even, last even digit)."""
        assert generate_integers(8, 8) == [8]

    def test_a_equals_b_equals_0(self):
        """Both bounds are 0 (even, first digit)."""
        assert generate_integers(0, 0) == [0]

    def test_reverse_with_boundary_values(self):
        """Reversed order with boundary values."""
        assert generate_integers(9, 0) == [0, 2, 4, 6, 8]

    def test_range_starting_at_8_ending_at_9(self):
        """Range [8, 9] contains only 8 as even."""
        assert generate_integers(8, 9) == [8]

    def test_range_starting_at_7_ending_at_8(self):
        """Range [7, 8] contains only 8 as even."""
        assert generate_integers(7, 8) == [8]

    def test_range_starting_at_8_ending_at_10(self):
        """Range [8, 10] capped at 10, only 8 is even."""
        assert generate_integers(8, 10) == [8]


class TestGenerateIntegers_EmptyAndZeroSize:
    """Tests with zero-size or empty-like inputs."""

    def test_identical_bounds_no_even(self):
        """Identical odd bounds produce empty result."""
        assert generate_integers(1, 1) == []

    def test_identical_bounds_no_even_large(self):
        """Identical large bounds produce empty result."""
        assert generate_integers(100, 100) == []

    def test_identical_bounds_even_large(self):
        """Identical large even bounds — still capped at 10, so empty."""
        assert generate_integers(100, 100) == []

    def test_wide_range_but_all_above_9(self):
        """Wide range entirely above single-digit numbers."""
        assert generate_integers(100, 200) == []

    def test_negative_and_positive(self):
        """Negative lower bound mixed with positive upper bound."""
        # range(-5, min(6, 10)) = range(-5, 6) → includes negatives
        result = generate_integers(-5, 6)
        assert result == [-4, -2, 0, 2, 4, 6]


class TestGenerateIntegers_InvalidInputs:
    """Tests with inputs outside documented constraints."""

    def test_negative_a_and_b(self):
        """Both inputs negative — code still runs without validation."""
        # swap not needed (-8 < -2), range(-8, min(-1, 10)) = range(-8, -1)
        # even numbers: -8, -6, -4, -2
        result = generate_integers(-8, -2)
        assert result == [-8, -6, -4, -2]

    def test_one_negative_one_positive(self):
        """One negative, one positive."""
        result = generate_integers(-3, 5)
        # swap not needed, range(-3, min(6, 10)) = range(-3, 6)
        assert result == [-2, 0, 2, 4]

    def test_very_large_numbers(self):
        """Very large numbers — both capped by min(b+1, 10)."""
        assert generate_integers(10**18, 10**18 + 1) == []

    def test_zero_as_first_argument(self):
        """Zero as first argument (not positive per docstring)."""
        assert generate_integers(0, 5) == [0, 2, 4]


class TestGenerateIntegers_ExceptionCases:
    """Tests where the function might raise exceptions."""

    def test_non_integer_string_input_raises(self):
        """Passing a string instead of an integer should raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers("2", "8")

    def test_list_input_raises(self):
        """Passing a list instead of an integer should raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers([2], [8])

    def test_none_input_raises(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers(None, None)

    def test_float_input_raises(self):
        """Passing float values should raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers(2.0, 8.0)

    def test_mixed_types_raises(self):
        """Mixing int and string should raise TypeError."""
        with pytest.raises(TypeError):
            generate_integers(2, "8")
