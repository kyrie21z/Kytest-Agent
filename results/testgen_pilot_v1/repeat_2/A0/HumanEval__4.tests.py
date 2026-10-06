import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_basic_example(self):
        """Test case from the docstring."""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_single_element(self):
        """A single element has MAD of 0 since |x - x| = 0."""
        assert mean_absolute_deviation([5.0]) == 0.0

    def test_two_elements(self):
        """For two elements, MAD is half the difference between them."""
        # |a - (a+b)/2| = |b-a|/2, same for b, so average = |b-a|/2
        assert mean_absolute_deviation([2.0, 6.0]) == 2.0

    def test_all_same_values(self):
        """When all values are identical, MAD should be 0."""
        assert mean_absolute_deviation([3.0, 3.0, 3.0, 3.0]) == 0.0

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # mean = (-1 + -2 + -3) / 3 = -2
        # MAD = (|-1 - (-2)| + |-2 - (-2)| + |-3 - (-2)|) / 3
        #     = (1 + 0 + 1) / 3 = 2/3
        result = mean_absolute_deviation([-1.0, -2.0, -3.0])
        assert result == pytest.approx(2.0 / 3.0)

    def test_mixed_positive_negative(self):
        """Test with a mix of positive and negative numbers."""
        # mean = (-2 + 0 + 2) / 3 = 0
        # MAD = (|-2| + |0| + |2|) / 3 = 4/3
        result = mean_absolute_deviation([-2.0, 0.0, 2.0])
        assert result == pytest.approx(4.0 / 3.0)

    def test_larger_dataset(self):
        """Test with a larger set of numbers."""
        # mean = (1+2+3+4+5)/5 = 3
        # MAD = (|1-3|+|2-3|+|3-3|+|4-3|+|5-3|)/5 = (2+1+0+1+2)/5 = 6/5 = 1.2
        result = mean_absolute_deviation([1.0, 2.0, 3.0, 4.0, 5.0])
        assert result == pytest.approx(1.2)

    def test_symmetric_data(self):
        """Symmetric data around the mean."""
        # mean = 0, MAD = (|−3|+|−1|+|0|+|1|+|3|)/5 = 8/5 = 1.6
        result = mean_absolute_deviation([-3.0, -1.0, 0.0, 1.0, 3.0])
        assert result == pytest.approx(1.6)

    def test_float_precision(self):
        """Test that floating point results are handled correctly."""
        # mean = 1.5
        # MAD = (|0.5-1.5| + |1.5-1.5| + |2.5-1.5|) / 3 = (1+0+1)/3 = 2/3
        result = mean_absolute_deviation([0.5, 1.5, 2.5])
        assert result == pytest.approx(2.0 / 3.0)

    def test_large_values(self):
        """Test with large magnitude numbers."""
        # mean = 500000
        # MAD = (|0-500000| + |1000000-500000|) / 2 = 500000
        assert mean_absolute_deviation([0.0, 1000000.0]) == 500000.0

    def test_empty_list_raises_error(self):
        """An empty list should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    def test_integer_input(self):
        """Test that integer inputs work correctly."""
        assert mean_absolute_deviation([1, 2, 3, 4]) == 1.0

    def test_duplicate_values(self):
        """Test with duplicate but not all-same values."""
        # mean = (1+1+2+2)/4 = 1.5
        # MAD = (|1-1.5|*2 + |2-1.5|*2) / 4 = (0.5*2 + 0.5*2) / 4 = 2/4 = 0.5
        result = mean_absolute_deviation([1, 1, 2, 2])
        assert result == pytest.approx(0.5)
