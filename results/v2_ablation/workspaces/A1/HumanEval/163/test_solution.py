"""Unit tests for generate_integers."""

import pytest
from solution import generate_integers


class TestDocstringExamples:
    """Tests directly from the docstring examples."""

    def test_basic_range(self):
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_swapped_inputs(self):
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_range_above_single_digits(self):
        assert generate_integers(10, 14) == []


class TestNormalCases:
    """Typical valid inputs within expected ranges."""

    def test_full_even_digit_range(self):
        """All even digits from 1 to 9."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_partial_range(self):
        """Range that includes some but not all even digits."""
        assert generate_integers(3, 7) == [4, 6]

    def test_start_at_first_even(self):
        assert generate_integers(2, 5) == [2, 4]

    def test_end_at_last_even(self):
        assert generate_integers(4, 8) == [4, 6, 8]

    def test_consecutive_evens(self):
        assert generate_integers(2, 4) == [2, 4]

    def test_only_odds_in_range(self):
        """Range containing only odd numbers."""
        assert generate_integers(3, 3) == []

    def test_mixed_odd_and_even(self):
        assert generate_integers(1, 5) == [2, 4]

    def test_equal_inputs_even(self):
        """Single even number as both bounds."""
        assert generate_integers(6, 6) == [6]

    def test_equal_inputs_odd(self):
        """Single odd number as both bounds."""
        assert generate_integers(7, 7) == []

    def test_a_equals_b_with_swap_needed(self):
        assert generate_integers(8, 8) == [8]


class TestBoundaryCases:
    """Edge-of-range inputs testing the clamping behavior at 10."""

    def test_upper_bound_exactly_10(self):
        """b+1 equals 10, so min(b+1, 10) = 10, range goes up to 9."""
        assert generate_integers(1, 10) == [2, 4, 6, 8]

    def test_lower_bound_at_10(self):
        """a is exactly 10, range starts at 10, clamped to 10 -> empty."""
        assert generate_integers(10, 10) == []

    def test_lower_bound_at_9(self):
        """a=9, b=9: range(9, 10) = [9], no evens."""
        assert generate_integers(9, 9) == []

    def test_lower_bound_at_8(self):
        """a=8, b=8: range(8, 9) = [8], one even."""
        assert generate_integers(8, 8) == [8]

    def test_large_b_clamped(self):
        """b is very large; result should be same as b=9."""
        assert generate_integers(1, 1000) == [2, 4, 6, 8]

    def test_large_a_and_b(self):
        """Both well above 10; range is empty."""
        assert generate_integers(100, 200) == []

    def test_a_below_10_b_well_above(self):
        """a is small, b is huge; clamped at 10."""
        assert generate_integers(5, 100) == [6, 8]

    def test_swapped_with_large_values(self):
        """Swap occurs, then clamping applies."""
        assert generate_integers(100, 5) == [6, 8]

    def test_a_is_0(self):
        """Lower bound 0: 0 is even, so it's included."""
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_range_from_0_to_0(self):
        assert generate_integers(0, 0) == [0]

    def test_range_from_0_to_2(self):
        assert generate_integers(0, 2) == [0, 2]


class TestNegativeInputs:
    """Inputs outside the documented 'positive integers' constraint."""

    def test_negative_a_positive_b(self):
        """Negative lower bound: negatives are even too."""
        result = generate_integers(-2, 5)
        # range(-2, min(6, 10)) = range(-2, 6) = [-2, -1, 0, 1, 2, 3, 4, 5]
        # evens: -2, 0, 2, 4
        assert result == [-2, 0, 2, 4]

    def test_both_negative(self):
        """Both negative: still works per implementation."""
        result = generate_integers(-6, -2)
        # range(-6, min(-1, 10)) = range(-6, -1) = [-6, -5, -4, -3, -2]
        # evens: -6, -4, -2
        assert result == [-6, -4, -2]

    def test_negative_swapped(self):
        """Swap with negatives."""
        result = generate_integers(-2, -6)
        # swap -> a=-6, b=-2
        # range(-6, min(-1, 10)) = range(-6, -1)
        # evens: -6, -4, -2
        assert result == [-6, -4, -2]


class TestZeroSizeAndEmptyResults:
    """Cases where the output is an empty list."""

    def test_no_evens_between_two_odds(self):
        assert generate_integers(3, 5) == [4]

    def test_adjacent_odds(self):
        assert generate_integers(3, 5) == [4]

    def test_same_odd_number(self):
        assert generate_integers(1, 1) == []

    def test_same_even_number(self):
        assert generate_integers(4, 4) == [4]

    def test_range_with_one_odd(self):
        assert generate_integers(5, 5) == []

    def test_all_numbers_above_ten(self):
        assert generate_integers(11, 19) == []

    def test_reverse_order_all_above_ten(self):
        assert generate_integers(19, 11) == []


class TestReturnValueType:
    """Verify the return type is always a list."""

    def test_returns_list(self):
        assert isinstance(generate_integers(2, 8), list)

    def test_empty_result_is_list(self):
        assert isinstance(generate_integers(10, 14), list)

    def test_single_element_is_list(self):
        assert isinstance(generate_integers(2, 2), list)
