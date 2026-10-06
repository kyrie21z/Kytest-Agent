import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_basic_example(self):
        """Test the doctest example: [1.0, 2.0, 3.0, 4.0] -> 1.0"""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_all_same_elements(self):
        """When all elements are the same, MAD should be 0."""
        assert mean_absolute_deviation([5.0, 5.0, 5.0, 5.0]) == 0.0

    def test_single_element(self):
        """A single element has MAD of 0."""
        assert mean_absolute_deviation([42.0]) == 0.0

    def test_two_elements(self):
        """With two elements, MAD is half the absolute difference."""
        # |3 - 5| + |7 - 5| = 2 + 2 = 4; 4 / 2 = 2.0
        assert mean_absolute_deviation([3.0, 7.0]) == 2.0

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # mean = (-3 + -1 + 1 + 3) / 4 = 0
        # MAD = (3 + 1 + 1 + 3) / 4 = 8 / 4 = 2.0
        assert mean_absolute_deviation([-3.0, -1.0, 1.0, 3.0]) == 2.0

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values."""
        # mean = (-2 + 0 + 2) / 3 = 0
        # MAD = (2 + 0 + 2) / 3 = 4/3
        result = mean_absolute_deviation([-2.0, 0.0, 2.0])
        assert abs(result - 4.0 / 3.0) < 1e-9

    def test_integer_input(self):
        """Test that integer inputs work correctly."""
        assert mean_absolute_deviation([1, 2, 3, 4]) == 1.0

    def test_larger_dataset(self):
        """Test with a larger dataset."""
        # Numbers 1 through 10
        numbers = list(range(1, 11))
        mean_val = sum(numbers) / len(numbers)  # 5.5
        mad = sum(abs(x - mean_val) for x in numbers) / len(numbers)
        assert abs(mean_absolute_deviation(numbers) - mad) < 1e-9

    def test_symmetric_data(self):
        """Symmetric data around zero."""
        # [-5, -3, 0, 3, 5], mean = 0
        # MAD = (5+3+0+3+5)/5 = 16/5 = 3.2
        assert mean_absolute_deviation([-5.0, -3.0, 0.0, 3.0, 5.0]) == 3.2

    def test_float_precision(self):
        """Test with floating point numbers that produce non-trivial results."""
        result = mean_absolute_deviation([1.5, 2.5, 3.5])
        # mean = 2.5, MAD = (1+0+1)/3 = 2/3
        assert abs(result - 2.0 / 3.0) < 1e-9

    def test_empty_list_raises_error(self):
        """Empty list should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    def test_single_negative_element(self):
        """Single negative element still has MAD of 0."""
        assert mean_absolute_deviation([-7.0]) == 0.0

    def test_widely_spaced_values(self):
        """Test with widely spaced values."""
        # [0, 100], mean = 50, MAD = (50+50)/2 = 50
        assert mean_absolute_deviation([0.0, 100.0]) == 50.0
