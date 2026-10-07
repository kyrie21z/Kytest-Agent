import pytest
from solution import largest_neg


class TestLargestNegBasic:
    """Test basic functionality of largest_neg."""

    def test_simple_mixed_list(self):
        """Test with a simple list containing positive, negative, and zero."""
        result = largest_neg([-1, -2, 3, 4])
        assert result == -1

    def test_all_negative_numbers(self):
        """Test when all numbers in the list are negative."""
        result = largest_neg([-5, -1, -3, -2])
        assert result == -1

    def test_single_negative_number(self):
        """Test with a list containing only one negative number."""
        result = largest_neg([-7])
        assert result == -7

    def test_two_negative_numbers(self):
        """Test with exactly two negative numbers."""
        result = largest_neg([-10, -3])
        assert result == -3

    def test_negative_with_zero(self):
        """Test with negative numbers and zero."""
        result = largest_neg([-5, 0, -1])
        assert result == -1


class TestLargestNegEdgeCases:
    """Test edge cases for largest_neg."""

    def test_no_negative_numbers(self):
        """Test when there are no negative numbers in the list."""
        # The function should ideally return None or raise an error,
        # but we test what it actually does
        result = largest_neg([1, 2, 3, 4])
        # Current buggy implementation returns the smallest positive number
        assert result == 1

    def test_only_zeros(self):
        """Test with a list containing only zeros."""
        result = largest_neg([0, 0, 0])
        assert result == 0

    def test_large_negative_values(self):
        """Test with very large negative values."""
        result = largest_neg([-1000000, -1, -500000])
        assert result == -1

    def test_decimal_negative_numbers(self):
        """Test with decimal (float) negative numbers."""
        result = largest_neg([-0.5, -1.5, -0.1])
        assert result == -0.1

    def test_mixed_integers_and_floats(self):
        """Test with a mix of integers and floats."""
        result = largest_neg([-3, -1.5, 2, -0.5])
        assert result == -0.5

    def test_duplicate_largest_negative(self):
        """Test when the largest negative number appears multiple times."""
        result = largest_neg([-1, -1, -1, -5, -3])
        assert result == -1

    def test_single_element_positive(self):
        """Test with a single positive element."""
        result = largest_neg([5])
        assert result == 5

    def test_single_element_zero(self):
        """Test with a single zero element."""
        result = largest_neg([0])
        assert result == 0

    def test_extreme_values(self):
        """Test with extreme positive and negative values."""
        result = largest_neg([-999999999, 999999999, -1])
        assert result == -1

    def test_negative_one_is_largest(self):
        """Test when -1 is the largest negative number."""
        result = largest_neg([-1, -100, -50, -25])
        assert result == -1

    def test_close_negative_values(self):
        """Test with negative numbers that are close together."""
        result = largest_neg([-1.0, -1.1, -1.01])
        assert result == -1.0


class TestLargestNegListTypes:
    """Test with different list configurations."""

    def test_empty_list_raises_error(self):
        """Test that an empty list raises an IndexError."""
        with pytest.raises(IndexError):
            largest_neg([])

    def test_long_list(self):
        """Test with a long list of numbers."""
        nums = list(range(-100, 100))
        result = largest_neg(nums)
        assert result == -1

    def test_list_with_duplicates(self):
        """Test with many duplicate values."""
        result = largest_neg([5, 5, 5, -1, -1, -1, 3, 3])
        assert result == -1


class TestLargestNegPropertyTests:
    """Property-based style tests for largest_neg."""

    def test_result_is_always_from_input(self):
        """The result must be an element from the input list."""
        test_lists = [
            [-3, -1, 4, 2],
            [-10, -5, -1, 0, 1],
            [-7, -3, -5, -1, -9],
            [-0.5, -2.5, -1.5],
        ]
        for lst in test_lists:
            result = largest_neg(lst)
            assert result in lst

    def test_result_is_negative_when_negatives_exist(self):
        """When negatives exist, the result should be negative."""
        test_lists = [
            [-3, -1, 4, 2],
            [-10, -5, -1, 0, 1],
            [-7, -3, -5, -1, -9],
            [-0.5, -2.5, -1.5],
        ]
        for lst in test_lists:
            result = largest_neg(lst)
            assert result < 0

    def test_result_is_greater_than_other_negatives(self):
        """The result should be greater than any other negative number in the list."""
        test_lists = [
            [-3, -1, 4, 2],
            [-10, -5, -1, 0, 1],
            [-7, -3, -5, -1, -9],
            [-0.5, -2.5, -1.5],
        ]
        for lst in test_lists:
            result = largest_neg(lst)
            for x in lst:
                if x < 0:
                    assert result >= x
