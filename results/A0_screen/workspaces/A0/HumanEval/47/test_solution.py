import pytest
from solution import median


class TestMedianBasic:
    """Test basic functionality of the median function."""

    def test_odd_length_list(self):
        """Test median with an odd number of elements."""
        assert median([3, 1, 2, 4, 5]) == 3

    def test_even_length_list(self):
        """Test median with an even number of elements."""
        # Sorted: [-10, 4, 6, 10, 20, 1000], middle elements are 6 and 10
        assert median([-10, 4, 6, 1000, 10, 20]) == 8.0

    def test_single_element(self):
        """Test median with a single element."""
        assert median([42]) == 42

    def test_two_elements(self):
        """Test median with exactly two elements."""
        assert median([1, 2]) == 1.5
        assert median([10, 30]) == 20.0
        assert median([5, 5]) == 5.0


class TestMedianEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_already_sorted(self):
        """Test median with an already sorted list."""
        assert median([1, 2, 3, 4, 5]) == 3

    def test_reverse_sorted(self):
        """Test median with a reverse-sorted list."""
        assert median([5, 4, 3, 2, 1]) == 3

    def test_all_same_elements(self):
        """Test median when all elements are identical."""
        assert median([7, 7, 7, 7, 7]) == 7
        assert median([3, 3]) == 3.0

    def test_duplicates(self):
        """Test median with duplicate values."""
        assert median([1, 2, 2, 3, 3]) == 2
        assert median([1, 1, 2, 2]) == 1.5

    def test_negative_numbers(self):
        """Test median with negative numbers."""
        assert median([-5, -3, -1, -4, -2]) == -3
        assert median([-10, -20, -30]) == -20

    def test_mixed_positive_negative(self):
        """Test median with mixed positive and negative numbers."""
        assert median([-5, 0, 5]) == 0
        assert median([-10, -5, 0, 5, 10]) == 0

    def test_large_numbers(self):
        """Test median with large numbers."""
        assert median([1000000, 2000000, 3000000]) == 2000000
        assert median([1, 1000000000, 2]) == 2

    def test_float_numbers(self):
        """Test median with floating-point numbers."""
        assert median([1.5, 2.5, 3.5]) == 2.5
        assert median([1.0, 2.0, 3.0, 4.0]) == 2.5

    def test_zero_in_list(self):
        """Test median when zero is present in the list."""
        assert median([0, 0, 0]) == 0
        assert median([-1, 0, 1]) == 0


class TestMedianReturnTypes:
    """Test that the return type is correct."""

    def test_odd_length_returns_int_for_int_list(self):
        """Odd-length integer list should return int."""
        result = median([3, 1, 2, 4, 5])
        assert isinstance(result, int)

    def test_even_length_returns_float_for_int_list(self):
        """Even-length integer list should return float."""
        result = median([1, 2])
        assert isinstance(result, float)

    def test_even_length_returns_float_for_float_list(self):
        """Even-length float list should return float."""
        result = median([1.0, 2.0])
        assert isinstance(result, float)

    def test_odd_length_returns_float_for_float_list(self):
        """Odd-length float list should return float."""
        result = median([1.0, 2.0, 3.0])
        assert isinstance(result, float)


class TestMedianDoctests:
    """Verify the doctest examples from the docstring."""

    def test_doctest_example_1(self):
        """First doctest example: [3, 1, 2, 4, 5] -> 3"""
        assert median([3, 1, 2, 4, 5]) == 3

    def test_doctest_example_2_corrected(self):
        """Second doctest example: [-10, 4, 6, 1000, 10, 20] -> 8.0
        Note: The docstring incorrectly states 15.0; the correct median is 8.0.
        Sorted: [-10, 4, 6, 10, 20, 1000], middle elements are 6 and 10.
        """
        assert median([-10, 4, 6, 1000, 10, 20]) == 8.0
