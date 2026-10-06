import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    # --- Docstring doctest example ---
    def test_basic_positive_numbers(self):
        """Test case from the docstring: [1, 2, 3, 4] -> 1.0"""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    # --- Edge cases ---
    def test_single_element(self):
        """A single element has MAD of 0 since |x - mean| = 0."""
        assert mean_absolute_deviation([5.0]) == 0.0

    def test_all_same_elements(self):
        """When all elements are identical, MAD is 0."""
        assert mean_absolute_deviation([3.0, 3.0, 3.0, 3.0]) == 0.0

    def test_empty_list_raises_error(self):
        """An empty list causes division by zero."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    # --- Negative and mixed numbers ---
    def test_negative_numbers(self):
        """Test with all negative numbers: [-1, -2, -3, -4] -> 1.0."""
        assert mean_absolute_deviation([-1.0, -2.0, -3.0, -4.0]) == 1.0

    def test_mixed_positive_and_negative(self):
        """Test with mixed signs: [-2, 0, 2] -> mean=0, MAD = (2+0+2)/3 = 4/3."""
        result = mean_absolute_deviation([-2.0, 0.0, 2.0])
        assert result == pytest.approx(4 / 3)

    def test_symmetric_around_zero(self):
        """Symmetric data around zero: [-3, -1, 1, 3] -> mean=0, MAD = 2.0."""
        assert mean_absolute_deviation([-3.0, -1.0, 1.0, 3.0]) == 2.0

    # --- Floating-point precision ---
    def test_float_values(self):
        """Test with non-integer floats."""
        result = mean_absolute_deviation([1.5, 2.5, 3.5])
        assert result == pytest.approx(0.6666666666666666)

    def test_small_decimal_values(self):
        """Test with small decimal values."""
        result = mean_absolute_deviation([0.1, 0.2, 0.3])
        assert result == pytest.approx(0.06666666666666667)

    # --- Larger datasets ---
    def test_two_elements(self):
        """Two elements: MAD = |a-b|/2."""
        assert mean_absolute_deviation([10.0, 20.0]) == 5.0

    def test_five_elements(self):
        """Five evenly spaced elements: [1, 2, 3, 4, 5] -> mean=3, MAD=1.2."""
        result = mean_absolute_deviation([1.0, 2.0, 3.0, 4.0, 5.0])
        assert result == pytest.approx(1.2)

    def test_large_dataset(self):
        """Test with a larger range of values."""
        numbers = list(range(1, 101))  # 1..100
        expected_mean = 50.5
        expected_mad = sum(abs(x - expected_mean) for x in numbers) / len(numbers)
        assert mean_absolute_deviation(numbers) == pytest.approx(expected_mad)

    # --- Verification against manual calculation ---
    def test_manual_calculation_verification(self):
        """Manually verify: [10, 20, 30] -> mean=20, MAD=(10+0+10)/3 = 20/3."""
        result = mean_absolute_deviation([10.0, 20.0, 30.0])
        assert result == pytest.approx(20 / 3)

    def test_all_zeros(self):
        """All zeros should yield MAD of 0."""
        assert mean_absolute_deviation([0.0, 0.0, 0.0]) == 0.0

    def test_large_values(self):
        """Test with large magnitude numbers.
        [1000, 2000, 3000] -> mean=2000, MAD=(1000+0+1000)/3 = 2000/3."""
        result = mean_absolute_deviation([1000.0, 2000.0, 3000.0])
        assert result == pytest.approx(2000 / 3)

    def test_negative_mean(self):
        """Test when the mean itself is negative."""
        result = mean_absolute_deviation([-10.0, -5.0, 0.0])
        # mean = -5, deviations = |(-10)-(-5)| + |(-5)-(-5)| + |0-(-5)| = 5+0+5 = 10
        # MAD = 10/3
        assert result == pytest.approx(10 / 3)
