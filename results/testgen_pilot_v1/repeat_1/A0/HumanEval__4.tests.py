import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_basic_example(self):
        """Test the doctest example: [1, 2, 3, 4] -> 1.0"""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_all_same_values(self):
        """When all values are identical, MAD should be 0."""
        assert mean_absolute_deviation([5.0, 5.0, 5.0, 5.0]) == 0.0

    def test_single_element(self):
        """A single-element list has MAD of 0."""
        assert mean_absolute_deviation([42.0]) == 0.0

    def test_two_elements(self):
        """Two elements: MAD is half the distance between them."""
        # mean = (1 + 9) / 2 = 5; MAD = (|1-5| + |9-5|) / 2 = (4+4)/2 = 4
        assert mean_absolute_deviation([1.0, 9.0]) == 4.0

    def test_negative_numbers(self):
        """MAD should work correctly with negative numbers."""
        # mean = (-2 + 0 + 2) / 3 = 0; MAD = (2 + 0 + 2) / 3 = 4/3
        result = mean_absolute_deviation([-2.0, 0.0, 2.0])
        assert abs(result - 4.0 / 3.0) < 1e-10

    def test_mixed_positive_and_negative(self):
        """Test with a mix of positive and negative values."""
        # mean = (-3 + 1 + 4 + 2) / 4 = 4/4 = 1
        # MAD = (|-3-1| + |1-1| + |4-1| + |2-1|) / 4 = (4+0+3+1)/4 = 8/4 = 2
        assert mean_absolute_deviation([-3.0, 1.0, 4.0, 2.0]) == 2.0

    def test_integers_as_input(self):
        """Function should handle integer inputs correctly."""
        assert mean_absolute_deviation([1, 2, 3, 4]) == 1.0

    def test_larger_dataset(self):
        """Test with a larger dataset."""
        # Numbers 1 through 10
        nums = list(range(1, 11))
        expected = sum(abs(x - 5.5) for x in nums) / 10.0
        assert abs(mean_absolute_deviation(nums) - expected) < 1e-10

    def test_symmetric_distribution(self):
        """Symmetric data around zero should have simple MAD."""
        # [-3, -2, -1, 0, 1, 2, 3], mean = 0
        # MAD = (3+2+1+0+1+2+3)/7 = 12/7
        result = mean_absolute_deviation([-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
        assert abs(result - 12.0 / 7.0) < 1e-10

    def test_decimal_values(self):
        """Test with decimal/fractional values."""
        # [0.5, 1.5, 2.5], mean = 1.5
        # MAD = (|0.5-1.5| + |1.5-1.5| + |2.5-1.5|) / 3 = (1+0+1)/3 = 2/3
        result = mean_absolute_deviation([0.5, 1.5, 2.5])
        assert abs(result - 2.0 / 3.0) < 1e-10

    def test_empty_list_raises_error(self):
        """Empty list should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    def test_large_values(self):
        """Test with large magnitude numbers."""
        # [1000, 2000, 3000], mean = 2000
        # MAD = (1000 + 0 + 1000) / 3 = 2000/3
        result = mean_absolute_deviation([1000.0, 2000.0, 3000.0])
        assert abs(result - 2000.0 / 3.0) < 1e-6

    def test_small_fractional_values(self):
        """Test with very small fractional values."""
        # [0.1, 0.2, 0.3], mean = 0.2
        # MAD = (0.1 + 0 + 0.1) / 3 = 0.2/3
        result = mean_absolute_deviation([0.1, 0.2, 0.3])
        assert abs(result - 0.2 / 3.0) < 1e-10
