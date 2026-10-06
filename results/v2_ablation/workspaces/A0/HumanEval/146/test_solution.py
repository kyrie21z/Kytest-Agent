import pytest
from solution import specialFilter


class TestSpecialFilter:
    """Tests for the specialFilter function."""

    def test_example_1(self):
        """Test case from docstring: [15, -73, 14, -15] => 1"""
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_2(self):
        """Test case from docstring: [33, -2, -3, 45, 21, 109] => 2"""
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_empty_list(self):
        """Empty list should return 0."""
        assert specialFilter([]) == 0

    def test_no_elements_match(self):
        """No elements satisfy the condition."""
        assert specialFilter([1, 2, 3, 10, -5, -10]) == 0

    def test_all_elements_match(self):
        """All elements satisfy the condition (all > 10, odd first and last digits)."""
        assert specialFilter([11, 13, 15, 17, 19, 31, 33, 35, 37, 39]) == 10

    def test_single_element_matches(self):
        """Single element that matches."""
        assert specialFilter([99]) == 1

    def test_single_element_does_not_match(self):
        """Single element that does not match."""
        assert specialFilter([5]) == 0

    def test_negative_numbers(self):
        """Negative numbers: str(num)[0] will be '-', so they never match."""
        assert specialFilter([-11, -13, -15, -99]) == 0

    def test_number_equal_to_10(self):
        """Number equal to 10 should not match (must be > 10)."""
        assert specialFilter([10]) == 0

    def test_first_digit_even(self):
        """First digit is even, should not match."""
        assert specialFilter([21, 23, 25, 27, 29]) == 0

    def test_last_digit_even(self):
        """Last digit is even, should not match."""
        assert specialFilter([12, 14, 16, 18, 32]) == 0

    def test_large_numbers(self):
        """Large numbers with odd first and last digits."""
        assert specialFilter([111, 113, 115, 117, 119]) == 5

    def test_mixed_positive_and_negative(self):
        """Mixed positive and negative numbers."""
        assert specialFilter([15, -73, 14, -15, 33, 45]) == 2

    def test_boundary_values(self):
        """Test boundary values around 10."""
        assert specialFilter([9, 10, 11]) == 1  # only 11 matches

    def test_returns_integer(self):
        """Ensure the return type is always int."""
        result = specialFilter([15, 33, 45])
        assert isinstance(result, int)

    def test_zero_is_integer(self):
        """Zero returned for empty list should be an int."""
        result = specialFilter([])
        assert isinstance(result, int)
        assert result == 0
