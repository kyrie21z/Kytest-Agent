import pytest
from solution import rolling_max


class TestRollingMax:
    """Tests for the rolling_max function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]

    def test_empty_list(self):
        """Test with an empty list."""
        assert rolling_max([]) == []

    def test_single_element(self):
        """Test with a single-element list."""
        assert rolling_max([5]) == [5]

    def test_increasing_sequence(self):
        """Test with a strictly increasing sequence."""
        assert rolling_max([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_decreasing_sequence(self):
        """Test with a strictly decreasing sequence."""
        assert rolling_max([5, 4, 3, 2, 1]) == [5, 5, 5, 5, 5]

    def test_all_same_elements(self):
        """Test with all identical elements."""
        assert rolling_max([3, 3, 3, 3]) == [3, 3, 3, 3]

    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert rolling_max([-3, -1, -2, -1, -5]) == [-3, -1, -1, -1, -1]

    def test_mixed_positive_and_negative(self):
        """Test with a mix of positive and negative numbers."""
        assert rolling_max([-1, 2, -3, 4, -5]) == [-1, 2, 2, 4, 4]

    def test_two_elements_increasing(self):
        """Test with two elements in increasing order."""
        assert rolling_max([1, 2]) == [1, 2]

    def test_two_elements_decreasing(self):
        """Test with two elements in decreasing order."""
        assert rolling_max([2, 1]) == [2, 2]

    def test_large_values(self):
        """Test with large integer values."""
        assert rolling_max([1000000, 2000000, 1500000]) == [1000000, 2000000, 2000000]

    def test_zeros(self):
        """Test with zeros."""
        assert rolling_max([0, 0, 0]) == [0, 0, 0]

    def test_alternating_pattern(self):
        """Test with an alternating up-down pattern."""
        assert rolling_max([1, 5, 2, 6, 3, 7]) == [1, 5, 5, 6, 6, 7]

    def test_return_type(self):
        """Ensure the return type is a list."""
        result = rolling_max([1, 2, 3])
        assert isinstance(result, list)

    def test_length_preserved(self):
        """Ensure output list has the same length as input."""
        assert len(rolling_max([1, 2, 3, 4])) == len([1, 2, 3, 4])
