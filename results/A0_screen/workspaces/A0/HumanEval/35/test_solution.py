import pytest
from solution import max_element


class TestMaxElement:
    """Unit tests for the max_element function."""

    def test_basic_positive_integers(self):
        """Test with a simple list of positive integers."""
        assert max_element([1, 2, 3]) == 3

    def test_mixed_numbers(self):
        """Test with a list containing positive, negative, and zero values."""
        assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123

    def test_single_element(self):
        """Test with a list containing only one element."""
        assert max_element([42]) == 42

    def test_max_at_beginning(self):
        """Test when the maximum element is at the start of the list."""
        assert max_element([100, 1, 2, 3]) == 100

    def test_max_at_end(self):
        """Test when the maximum element is at the end of the list."""
        assert max_element([1, 2, 3, 100]) == 100

    def test_max_in_middle(self):
        """Test when the maximum element is somewhere in the middle."""
        assert max_element([1, 50, 3]) == 50

    def test_all_same_elements(self):
        """Test with a list where all elements are identical."""
        assert max_element([7, 7, 7, 7]) == 7

    def test_negative_numbers_only(self):
        """Test with a list containing only negative numbers."""
        assert max_element([-1, -2, -3, -4]) == -1

    def test_two_elements(self):
        """Test with a list containing exactly two elements."""
        assert max_element([10, 20]) == 20
        assert max_element([20, 10]) == 20

    def test_large_numbers(self):
        """Test with very large integer values."""
        assert max_element([10**9, 10**8, 10**10]) == 10**10

    def test_duplicate_maximum(self):
        """Test when the maximum value appears multiple times."""
        assert max_element([5, 10, 5, 10, 3]) == 10

    def test_float_values(self):
        """Test with floating point numbers."""
        assert max_element([1.5, 2.7, 3.1, 0.5]) == 3.1

    def test_zero_and_negatives(self):
        """Test with zero and negative numbers."""
        assert max_element([0, -1, -2, -3]) == 0

    def test_docstring_example_1(self):
        """Verify the first example from the docstring."""
        assert max_element([1, 2, 3]) == 3

    def test_docstring_example_2(self):
        """Verify the second example from the docstring."""
        assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123

    def test_empty_list_raises_error(self):
        """Test that an empty list raises ValueError (as expected by built-in max)."""
        with pytest.raises(ValueError):
            max_element([])
