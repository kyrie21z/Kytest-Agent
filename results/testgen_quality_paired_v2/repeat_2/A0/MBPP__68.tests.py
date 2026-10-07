import pytest
from solution import is_Monotonic


class TestIsMonotonic:
    """Unit tests for the is_Monotonic function."""

    def test_empty_array(self):
        """An empty array is trivially monotonic."""
        assert is_Monotonic([]) is True

    def test_single_element(self):
        """A single-element array is monotonic."""
        assert is_Monotonic([1]) is True

    def test_two_elements_increasing(self):
        """Two elements in increasing order are monotonic."""
        assert is_Monotonic([1, 2]) is True

    def test_two_elements_decreasing(self):
        """Two elements in decreasing order are monotonic."""
        assert is_Monotonic([2, 1]) is True

    def test_two_elements_equal(self):
        """Two equal elements are monotonic."""
        assert is_Monotonic([3, 3]) is True

    def test_strictly_increasing(self):
        """A strictly increasing array is monotonic."""
        assert is_Monotonic([1, 2, 3, 4, 5]) is True

    def test_strictly_decreasing(self):
        """A strictly decreasing array is monotonic."""
        assert is_Monotonic([5, 4, 3, 2, 1]) is True

    def test_constant_array(self):
        """A constant array is monotonic."""
        assert is_Monotonic([7, 7, 7, 7]) is True

    def test_non_decreasing_with_duplicates(self):
        """A non-decreasing array with duplicates is monotonic."""
        assert is_Monotonic([1, 2, 2, 3, 3, 4]) is True

    def test_non_increasing_with_duplicates(self):
        """A non-increasing array with duplicates is monotonic."""
        assert is_Monotonic([5, 4, 4, 3, 2, 2]) is True

    def test_not_monotonic_increasing_then_decreasing(self):
        """Array that increases then decreases is not monotonic."""
        assert is_Monotonic([1, 3, 2]) is False

    def test_not_monotonic_decreasing_then_increasing(self):
        """Array that decreases then increases is not monotonic."""
        assert is_Monotonic([5, 2, 4]) is False

    def test_not_monotonic_v_shape(self):
        """V-shaped array is not monotonic."""
        assert is_Monotonic([3, 1, 2]) is False

    def test_not_monotonic_inverted_v_shape(self):
        """Inverted V-shaped array is not monotonic."""
        assert is_Monotonic([1, 5, 2]) is False

    def test_negative_numbers_increasing(self):
        """Negative numbers in increasing order are monotonic."""
        assert is_Monotonic([-5, -3, -1, 0, 2]) is True

    def test_negative_numbers_decreasing(self):
        """Negative numbers in decreasing order are monotonic."""
        assert is_Monotonic([2, 0, -1, -3, -5]) is True

    def test_mixed_positive_negative_not_monotonic(self):
        """Mixed positive and negative numbers that change direction are not monotonic."""
        assert is_Monotonic([-1, 3, -2]) is False

    def test_all_same_large_array(self):
        """Large constant array is monotonic."""
        assert is_Monotonic([0] * 1000) is True

    def test_fluctuating_array(self):
        """Highly fluctuating array is not monotonic."""
        assert is_Monotonic([1, 3, 2, 4, 1, 5]) is False

    def test_sorted_ascending_large(self):
        """Large sorted ascending array is monotonic."""
        assert is_Monotonic(list(range(100))) is True

    def test_sorted_descending_large(self):
        """Large sorted descending array is monotonic."""
        assert is_Monotonic(list(range(100, 0, -1))) is True
