import pytest
from solution import incr_list


class TestIncrList:
    """Unit tests for the incr_list function."""

    def test_basic_increment(self):
        """Test basic increment of a list of positive integers."""
        assert incr_list([1, 2, 3]) == [2, 3, 4]

    def test_doctest_example_2(self):
        """Test the second doctest example."""
        assert incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [6, 4, 6, 3, 4, 4, 10, 1, 124]

    def test_empty_list(self):
        """Test that an empty list returns an empty list."""
        assert incr_list([]) == []

    def test_single_element(self):
        """Test incrementing a list with a single element."""
        assert incr_list([7]) == [8]

    def test_negative_numbers(self):
        """Test incrementing a list containing negative numbers."""
        assert incr_list([-5, -3, -1]) == [-4, -2, 0]

    def test_mixed_positive_and_negative(self):
        """Test incrementing a list with both positive and negative numbers."""
        assert incr_list([-2, 0, 2]) == [-1, 1, 3]

    def test_zero_in_list(self):
        """Test that zero is correctly incremented to one."""
        assert incr_list([0]) == [1]

    def test_large_numbers(self):
        """Test incrementing a list with large numbers."""
        assert incr_list([1000000, 999999999]) == [1000001, 1000000000]

    def test_all_zeros(self):
        """Test incrementing a list of all zeros."""
        assert incr_list([0, 0, 0]) == [1, 1, 1]

    def test_duplicate_elements(self):
        """Test that duplicate elements are each incremented independently."""
        assert incr_list([4, 4, 4]) == [5, 5, 5]

    def test_returns_new_list(self):
        """Test that the original list is not modified."""
        original = [1, 2, 3]
        result = incr_list(original)
        assert result == [2, 3, 4]
        assert original == [1, 2, 3]

    def test_result_is_different_object(self):
        """Test that the returned list is a new object, not the same reference."""
        original = [1, 2, 3]
        result = incr_list(original)
        assert result is not original

    def test_float_values(self):
        """Test incrementing a list with float values."""
        assert incr_list([1.5, 2.5, 3.5]) == [2.5, 3.5, 4.5]

    def test_single_zero(self):
        """Test incrementing a list containing only zero."""
        assert incr_list([0]) == [1]

    def test_descending_order(self):
        """Test incrementing a descending-ordered list."""
        assert incr_list([5, 4, 3, 2, 1]) == [6, 5, 4, 3, 2]
