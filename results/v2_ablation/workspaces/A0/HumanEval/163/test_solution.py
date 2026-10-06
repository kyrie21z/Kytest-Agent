import pytest
from solution import generate_integers


class TestGenerateIntegers:
    """Tests for the generate_integers function."""

    # --- Docstring examples ---

    def test_basic_range(self):
        """Example from docstring: generate_integers(2, 8) => [2, 4, 6, 8]"""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_swapped_order(self):
        """Example from docstring: generate_integers(8, 2) => [2, 4, 6, 8]"""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_no_even_digits(self):
        """Example from docstring: generate_integers(10, 14) => []"""
        assert generate_integers(10, 14) == []

    # --- Swapping behavior ---

    def test_equal_values(self):
        """When a == b, the range is just that single value."""
        assert generate_integers(4, 4) == [4]
        assert generate_integers(5, 5) == []

    def test_a_greater_than_b(self):
        """Ensure swapping works correctly for various ranges."""
        assert generate_integers(9, 1) == [2, 4, 6, 8]
        assert generate_integers(7, 3) == [4, 6]

    # --- Single-digit ranges ---

    def test_range_starting_at_one(self):
        """Range starting at 1 should include 2, 4, 6, 8."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_range_with_only_odd_numbers(self):
        """Range containing only odd numbers returns empty list."""
        assert generate_integers(1, 1) == []
        assert generate_integers(3, 3) == []
        assert generate_integers(5, 5) == []

    def test_single_even_digit(self):
        """Range containing exactly one even digit."""
        assert generate_integers(2, 2) == [2]
        assert generate_integers(4, 4) == [4]
        assert generate_integers(6, 6) == [6]
        assert generate_integers(8, 8) == [8]

    def test_two_consecutive_evens(self):
        """Range spanning two consecutive even digits."""
        assert generate_integers(2, 4) == [2, 4]
        assert generate_integers(4, 6) == [4, 6]
        assert generate_integers(6, 8) == [6, 8]

    # --- Multi-digit inputs ---

    def test_both_inputs_multi_digit(self):
        """Both inputs are multi-digit; result should be empty."""
        assert generate_integers(10, 20) == []
        assert generate_integers(100, 200) == []

    def test_one_multi_digit_one_single(self):
        """One input is multi-digit, the other is single-digit."""
        assert generate_integers(1, 15) == [2, 4, 6, 8]
        assert generate_integers(15, 1) == [2, 4, 6, 8]

    def test_boundary_at_ten(self):
        """Range ending exactly at 10 should not include 10 (not a digit)."""
        assert generate_integers(1, 10) == [2, 4, 6, 8]

    def test_large_range(self):
        """Large range should still only return single-digit even numbers."""
        assert generate_integers(0, 1000) == [0, 2, 4, 6, 8]

    # --- Edge cases ---

    def test_minimal_positive_range(self):
        """Smallest possible positive integer range."""
        assert generate_integers(1, 2) == [2]

    def test_even_number_not_in_range(self):
        """Even number outside the range should not appear."""
        assert generate_integers(1, 3) == [2]
        assert generate_integers(5, 5) == []

    def test_result_is_sorted(self):
        """Result should always be in ascending order regardless of input order."""
        assert generate_integers(8, 2) == sorted(generate_integers(8, 2))
        assert generate_integers(1, 9) == sorted(generate_integers(1, 9))

    def test_empty_result_for_non_overlapping(self):
        """Range entirely above single digits yields empty list."""
        assert generate_integers(11, 99) == []
