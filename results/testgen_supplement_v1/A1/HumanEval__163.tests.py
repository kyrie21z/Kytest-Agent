"""Unit tests for generate_integers."""

import pytest
from solution import generate_integers


class TestDocstringExamples:
    """Tests directly from the docstring examples."""

    def test_basic_range(self):
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_reversed_order(self):
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_no_even_digits_in_range(self):
        assert generate_integers(10, 14) == []


class TestNormalCases:
    """Typical valid inputs covering various ranges."""

    def test_full_single_digit_range(self):
        """All single-digit numbers; should return all even digits."""
        assert generate_integers(0, 9) == [0, 2, 4, 6, 8]

    def test_partial_odd_start(self):
        """Range starting at odd number."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_narrow_range(self):
        """Small range containing some even numbers."""
        assert generate_integers(3, 7) == [4, 6]

    def test_reverse_narrow_range(self):
        """Small range with a > b."""
        assert generate_integers(7, 3) == [4, 6]

    def test_range_with_only_one_even(self):
        """Range containing exactly one even number."""
        assert generate_integers(1, 3) == [2]

    def test_range_at_upper_boundary(self):
        """Range ending at 10 (exclusive due to min cap)."""
        assert generate_integers(0, 10) == [0, 2, 4, 6, 8]

    def test_range_extending_beyond_10(self):
        """Upper bound far beyond 10; still capped at 10."""
        assert generate_integers(0, 100) == [0, 2, 4, 6, 8]

    def test_lower_bound_above_10(self):
        """Both bounds above 10; no single-digit evens exist."""
        assert generate_integers(11, 20) == []

    def test_both_bounds_above_10_reversed(self):
        """Both bounds above 10, reversed order."""
        assert generate_integers(20, 11) == []

    def test_range_just_below_10(self):
        """Range ending just below 10."""
        assert generate_integers(8, 10) == [8]

    def test_range_starting_at_8(self):
        assert generate_integers(8, 9) == [8]

    def test_range_starting_at_6(self):
        assert generate_integers(6, 9) == [6, 8]

    def test_range_starting_at_4(self):
        assert generate_integers(4, 9) == [4, 6, 8]

    def test_range_starting_at_2(self):
        assert generate_integers(2, 9) == [2, 4, 6, 8]


class TestBoundaryCases:
    """Edge cases at boundaries of valid input ranges."""

    def test_same_even_number_a_equals_b(self):
        """Single even number as both bounds."""
        assert generate_integers(2, 2) == [2]

    def test_same_even_number_reversed(self):
        assert generate_integers(2, 2) == [2]

    def test_same_odd_number_a_equals_b(self):
        """Single odd number as both bounds."""
        assert generate_integers(3, 3) == []

    def test_zero_as_lower_bound(self):
        """0 is an even digit."""
        assert generate_integers(0, 0) == [0]

    def test_zero_in_range(self):
        """Range includes 0."""
        assert generate_integers(0, 5) == [0, 2, 4]

    def test_adjacent_numbers_both_even(self):
        """Two consecutive even numbers."""
        assert generate_integers(4, 6) == [4, 6]

    def test_adjacent_numbers_one_even_one_odd(self):
        assert generate_integers(3, 4) == [4]

    def test_adjacent_numbers_both_odd(self):
        assert generate_integers(3, 5) == [4]

    def test_large_gap_all_evens(self):
        """Large gap within single digits."""
        assert generate_integers(0, 8) == [0, 2, 4, 6, 8]

    def test_exclusive_upper_bound_behavior(self):
        """Verify b is exclusive in the range (standard Python range semantics)."""
        # range(2, min(8+1, 10)) = range(2, 9) -> 2,3,4,5,6,7,8
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_upper_bound_exactly_10(self):
        """b=10 means min(11, 10)=10, so range goes up to 9 inclusive."""
        assert generate_integers(0, 10) == [0, 2, 4, 6, 8]

    def test_upper_bound_11(self):
        """b=11 means min(12, 10)=10, same as b=10."""
        assert generate_integers(0, 11) == [0, 2, 4, 6, 8]


class TestEmptyAndZeroSizeInputs:
    """Cases where the result is empty or inputs are minimal."""

    def test_empty_result_consecutive_odds(self):
        """Range of consecutive odd numbers yields empty list."""
        assert generate_integers(1, 3) == [2]  # Actually contains 2

    def test_empty_result_no_evens(self):
        """Range with no even numbers."""
        assert generate_integers(1, 1) == []

    def test_empty_result_high_range(self):
        """High range with no single-digit numbers."""
        assert generate_integers(100, 200) == []

    def test_empty_result_negative_to_negative(self):
        """Negative range — implementation allows it; check behavior."""
        result = generate_integers(-5, -1)
        # range(-5, min(0, 10)) = range(-5, 0) -> -5,-4,-3,-2,-1
        # Even negatives: -4, -2
        assert result == [-4, -2]

    def test_empty_result_both_zero(self):
        """Both bounds are zero."""
        assert generate_integers(0, 0) == [0]


class TestInvalidInputs:
    """Inputs outside documented constraints (positive integers).
    
    The docstring says "positive integers" but the function does not
    validate or raise on invalid input. These tests verify graceful
    handling / actual behavior.
    """

    def test_negative_a_positive_b(self):
        """Negative lower bound, positive upper bound."""
        result = generate_integers(-2, 5)
        # After swap? No: -2 < 5, so no swap.
        # range(-2, min(6, 10)) = range(-2, 6) -> -2,-1,0,1,2,3,4,5
        # Evens: -2, 0, 2, 4
        assert result == [-2, 0, 2, 4]

    def test_both_negative(self):
        """Both arguments negative."""
        result = generate_integers(-8, -2)
        # range(-8, min(-1, 10)) = range(-8, -1) -> -8,-7,...,-2
        # Evens: -8, -6, -4, -2
        assert result == [-8, -6, -4, -2]

    def test_both_negative_reversed(self):
        """Both negative, a > b."""
        result = generate_integers(-2, -8)
        # Swap: a=-8, b=-2
        # range(-8, min(-1, 10)) = range(-8, -1) -> -8,-7,...,-2
        # Evens: -8, -6, -4, -2
        assert result == [-8, -6, -4, -2]

    def test_zero_and_negative(self):
        """One zero, one negative."""
        result = generate_integers(-3, 0)
        # range(-3, min(1, 10)) = range(-3, 1) -> -3,-2,-1,0
        # Evens: -2, 0
        assert result == [-2, 0]

    def test_zero_and_negative_reversed(self):
        result = generate_integers(0, -3)
        # Swap: a=-3, b=0
        # range(-3, min(1, 10)) = range(-3, 1) -> -3,-2,-1,0
        # Evens: -2, 0
        assert result == [-2, 0]


class TestReturnProperties:
    """Tests verifying structural properties of the output."""

    def test_output_is_always_sorted(self):
        """Output should always be in ascending order."""
        for a, b in [(2, 8), (8, 2), (0, 9), (3, 7), (-5, 5), (100, 200)]:
            result = generate_integers(a, b)
            assert result == sorted(result), f"Not sorted for ({a}, {b})"

    def test_output_contains_only_even_numbers(self):
        """Every element must be even."""
        for a, b in [(2, 8), (8, 2), (0, 9), (3, 7), (-5, 5), (100, 200)]:
            result = generate_integers(a, b)
            for n in result:
                assert n % 2 == 0, f"Odd number {n} found in result for ({a}, {b})"

    def test_output_contains_only_single_digit_non_negatives_when_bounds_positive(self):
        """When both bounds are positive, output should only contain 0-8."""
        for a, b in [(0, 9), (1, 9), (2, 8), (0, 100)]:
            result = generate_integers(a, b)
            for n in result:
                assert 0 <= n <= 8, f"Number {n} out of expected range for ({a}, {b})"

    def test_return_type_is_list(self):
        """Ensure the return type is always a list."""
        assert isinstance(generate_integers(2, 8), list)
        assert isinstance(generate_integers(10, 14), list)
        assert isinstance(generate_integers(0, 0), list)
