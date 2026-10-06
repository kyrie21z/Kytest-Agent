import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_docstring_example(self):
        """Test the example given in the docstring."""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_single_element(self):
        """A single-element list has MAD of 0 since |x - mean| = 0."""
        assert mean_absolute_deviation([5.0]) == 0.0

    def test_two_elements(self):
        """For [a, b], mean = (a+b)/2, MAD = |a-b|/2."""
        assert mean_absolute_deviation([1.0, 3.0]) == 1.0

    def test_all_same_elements(self):
        """When all elements are identical, MAD is 0."""
        assert mean_absolute_deviation([7.0, 7.0, 7.0, 7.0]) == 0.0

    def test_symmetric_data(self):
        """Symmetric data around zero: [-2, -1, 0, 1, 2] -> MAD = 1.2."""
        result = mean_absolute_deviation([-2.0, -1.0, 0.0, 1.0, 2.0])
        assert result == pytest.approx(1.2)

    def test_negative_numbers(self):
        """Test with negative numbers: [-1, 0, 1] -> MAD = 2/3."""
        result = mean_absolute_deviation([-1.0, 0.0, 1.0])
        assert result == pytest.approx(2.0 / 3.0)

    def test_positive_integers(self):
        """Test with consecutive positive integers [1, 2, 3]."""
        # mean = 2.0, MAD = (|1-2| + |2-2| + |3-2|) / 3 = 2/3
        result = mean_absolute_deviation([1, 2, 3])
        assert result == pytest.approx(2.0 / 3.0)

    def test_larger_dataset(self):
        """Test with a larger set of values."""
        # [10, 20, 30, 40, 50] -> mean = 30
        # MAD = (20 + 10 + 0 + 10 + 20) / 5 = 60/5 = 12.0
        result = mean_absolute_deviation([10.0, 20.0, 30.0, 40.0, 50.0])
        assert result == 12.0

    def test_mixed_values(self):
        """Test with mixed positive and negative floating-point values."""
        # [-1.5, 0.5, 2.5] -> mean = 0.5
        # MAD = (|-1.5-0.5| + |0.5-0.5| + |2.5-0.5|) / 3 = (2.0 + 0 + 2.0) / 3 = 4/3
        result = mean_absolute_deviation([-1.5, 0.5, 2.5])
        assert result == pytest.approx(4.0 / 3.0)

    def test_large_values(self):
        """Test with large magnitude numbers."""
        # [1000, 2000, 3000] -> mean = 2000
        # MAD = (1000 + 0 + 1000) / 3 = 2000/3
        result = mean_absolute_deviation([1000.0, 2000.0, 3000.0])
        assert result == pytest.approx(2000.0 / 3.0)

    def test_small_decimal_values(self):
        """Test with small decimal values."""
        # [0.1, 0.2, 0.3] -> mean = 0.2
        # MAD = (0.1 + 0 + 0.1) / 3 = 0.2/3
        result = mean_absolute_deviation([0.1, 0.2, 0.3])
        assert result == pytest.approx(0.2 / 3.0)

    def test_returns_float(self):
        """Ensure the return type is float even with integer inputs."""
        result = mean_absolute_deviation([1, 2, 3])
        assert isinstance(result, float)

    def test_empty_list_raises_error(self):
        """An empty list should raise a ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])
