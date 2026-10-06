import pytest
from solution import generate_integers


class TestGenerateIntegers:
    """Unit tests for generate_integers function."""

    # --- Docstring examples ---

    def test_example_1(self):
        """Example from docstring: generate_integers(2, 8) => [2, 4, 6, 8]"""
        assert generate_integers(2, 8) == [2, 4, 6, 8]

    def test_example_2(self):
        """Example from docstring: generate_integers(8, 2) => [2, 4, 6, 8]"""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_example_3(self):
        """Example from docstring: generate_integers(10, 14) => []"""
        assert generate_integers(10, 14) == []

    # --- Basic functionality: a < b ---

    def test_basic_range(self):
        """Even numbers in a normal ascending range."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_single_even_number(self):
        """Range containing exactly one even number."""
        assert generate_integers(2, 2) == [2]

    def test_no_even_numbers(self):
        """Range with no even numbers."""
        assert generate_integers(1, 1) == []

    def test_odd_to_odd_range(self):
        """Range starting and ending on odd numbers."""
        assert generate_integers(3, 7) == [4, 6]

    def test_even_to_even_range(self):
        """Range starting and ending on even numbers."""
        assert generate_integers(2, 6) == [2, 4, 6]

    # --- Reversed input: a > b ---

    def test_reversed_input(self):
        """Function should handle a > b by swapping."""
        assert generate_integers(8, 2) == [2, 4, 6, 8]

    def test_reversed_equal(self):
        """Equal inputs with a > b swap logic."""
        assert generate_integers(5, 5) == []

    def test_reversed_large_range(self):
        """Reversed large range."""
        assert generate_integers(9, 1) == [2, 4, 6, 8]

    # --- Boundary conditions ---

    def test_min_boundary(self):
        """Test with minimum positive integer."""
        assert generate_integers(1, 2) == [2]

    def test_max_single_digit(self):
        """Test up to max single digit (9)."""
        assert generate_integers(1, 9) == [2, 4, 6, 8]

    def test_exactly_at_ten(self):
        """Range that includes 10 — only single digits returned."""
        assert generate_integers(8, 10) == [8]

    def test_starting_at_ten(self):
        """Starting at 10 yields no single-digit evens."""
        assert generate_integers(10, 10) == []

    def test_ending_at_ten(self):
        """Ending at 10 still capped at single digits."""
        assert generate_integers(1, 10) == [2, 4, 6, 8]

    def test_both_above_ten(self):
        """Both arguments above 10 yield empty list."""
        assert generate_integers(10, 20) == []

    def test_one_above_ten(self):
        """One argument above 10, other below."""
        assert generate_integers(5, 15) == [6, 8]

    # --- Edge cases ---

    def test_identical_inputs(self):
        """Same value for both a and b."""
        assert generate_integers(4, 4) == [4]

    def test_identical_odd(self):
        """Same odd value for both a and b."""
        assert generate_integers(3, 3) == []

    def test_adjacent_numbers(self):
        """Adjacent even numbers."""
        assert generate_integers(4, 5) == [4]

    def test_adjacent_numbers_reverse(self):
        """Adjacent numbers in reverse."""
        assert generate_integers(5, 4) == [4]

    def test_zero_in_range(self):
        """Range that would include 0 — but 0 is even."""
        # Since 0 is an even digit, check behavior
        result = generate_integers(0, 5)
        assert 0 in result
        assert result == [0, 2, 4]

    def test_large_gap(self):
        """Large gap between a and b."""
        assert generate_integers(1, 100) == [2, 4, 6, 8]

    def test_negative_handling(self):
        """Negative numbers — function uses min(b+1, 10) so results may vary."""
        # With negative a, range starts from negative; but only single digits <= 9 considered
        result = generate_integers(-2, 5)
        # range(-2, 6) gives [-2, -1, 0, 1, 2, 3, 4, 5]; even ones: -2, 0, 2, 4
        assert result == [-2, 0, 2, 4]

    # --- Return type checks ---

    def test_returns_list(self):
        """Ensure the return type is a list."""
        assert isinstance(generate_integers(1, 9), list)

    def test_returns_sorted(self):
        """Ensure results are always in ascending order."""
        result = generate_integers(8, 2)
        assert result == sorted(result)

    def test_no_duplicates(self):
        """Ensure no duplicate values in result."""
        result = generate_integers(1, 9)
        assert len(result) == len(set(result))
