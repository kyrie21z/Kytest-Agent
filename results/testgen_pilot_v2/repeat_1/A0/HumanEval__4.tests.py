import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_docstring_example(self):
        """Test the example given in the docstring."""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_single_element(self):
        """A single element has MAD of 0 (no deviation)."""
        assert mean_absolute_deviation([5.0]) == 0.0

    def test_two_elements(self):
        """With two elements, MAD equals half their difference."""
        # |x - mean| + |y - mean| = |x - y| / 2 + |y - x| / 2 = |x - y|
        # MAD = |x - y| / 2
        assert mean_absolute_deviation([2.0, 6.0]) == 2.0

    def test_all_same_values(self):
        """When all values are identical, MAD is 0."""
        assert mean_absolute_deviation([7.0, 7.0, 7.0, 7.0]) == 0.0

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # mean = (-3 + -1 + 1 + 3) / 4 = 0
        # MAD = (3 + 1 + 1 + 3) / 4 = 2.0
        assert mean_absolute_deviation([-3.0, -1.0, 1.0, 3.0]) == 2.0

    def test_mixed_positive_negative(self):
        """Test with a mix of positive and negative numbers."""
        # mean = (1 + -2 + 3 + -4 + 5) / 5 = 3/5 = 0.6
        # deviations = |1-0.6| + |-2-0.6| + |3-0.6| + |-4-0.6| + |5-0.6|
        #            = 0.4 + 2.6 + 2.4 + 4.6 + 4.4 = 14.4
        # MAD = 14.4 / 5 = 2.88
        assert mean_absolute_deviation([1.0, -2.0, 3.0, -4.0, 5.0]) == 2.88

    def test_symmetric_data(self):
        """Symmetric data around the mean."""
        # mean = 0, symmetric pairs => MAD = average of absolute values
        result = mean_absolute_deviation([-2.0, -1.0, 0.0, 1.0, 2.0])
        assert result == 1.2

    def test_large_numbers(self):
        """Test with large magnitude numbers."""
        # mean = (1000 + 2000 + 3000) / 3 = 2000
        # MAD = (1000 + 0 + 1000) / 3 = 2000/3
        expected = 2000.0 / 3.0
        assert abs(mean_absolute_deviation([1000.0, 2000.0, 3000.0]) - expected) < 1e-9

    def test_small_decimal_numbers(self):
        """Test with small decimal values."""
        # mean = (0.1 + 0.2 + 0.3) / 3 = 0.2
        # MAD = (0.1 + 0.0 + 0.1) / 3 = 0.2/3
        expected = 0.2 / 3.0
        assert abs(mean_absolute_deviation([0.1, 0.2, 0.3]) - expected) < 1e-9

    def test_integer_input(self):
        """Test that integer inputs work correctly."""
        assert mean_absolute_deviation([1, 2, 3, 4]) == 1.0

    def test_even_number_of_elements(self):
        """Test with an even number of elements."""
        # [1, 2, 3, 4, 5, 6] -> mean = 3.5
        # MAD = (2.5 + 1.5 + 0.5 + 0.5 + 1.5 + 2.5) / 6 = 9/6 = 1.5
        assert mean_absolute_deviation([1, 2, 3, 4, 5, 6]) == 1.5

    def test_odd_number_of_elements(self):
        """Test with an odd number of elements."""
        # [10, 20, 30] -> mean = 20
        # MAD = (10 + 0 + 10) / 3 = 20/3
        expected = 20.0 / 3.0
        assert abs(mean_absolute_deviation([10, 20, 30]) - expected) < 1e-9

    def test_empty_list_raises_error(self):
        """An empty list should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    def test_return_type_is_float(self):
        """Ensure the return type is float."""
        result = mean_absolute_deviation([1.0, 2.0, 3.0])
        assert isinstance(result, float)

    def test_three_identical_elements(self):
        """Three identical elements should yield MAD of 0."""
        assert mean_absolute_deviation([42.0, 42.0, 42.0]) == 0.0

    def test_widely_spaced_values(self):
        """Test with widely spread values."""
        # mean = (0 + 100) / 2 = 50
        # MAD = (50 + 50) / 2 = 50
        assert mean_absolute_deviation([0.0, 100.0]) == 50.0
