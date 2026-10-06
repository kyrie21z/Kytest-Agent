import pytest
from solution import mean_absolute_deviation


class TestMeanAbsoluteDeviation:
    """Tests for the mean_absolute_deviation function."""

    def test_basic_example(self):
        """Test the example from the docstring."""
        assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0

    def test_single_element(self):
        """MAD of a single element is always 0."""
        assert mean_absolute_deviation([5.0]) == 0.0

    def test_two_identical_elements(self):
        """All same values should yield MAD of 0."""
        assert mean_absolute_deviation([3.0, 3.0, 3.0]) == 0.0

    def test_symmetric_values(self):
        """Symmetric distribution around the mean."""
        # Mean = 0, elements are -2, -1, 0, 1, 2 => MAD = (2+1+0+1+2)/5 = 1.2
        assert mean_absolute_deviation([-2.0, -1.0, 0.0, 1.0, 2.0]) == 1.2

    def test_negative_numbers(self):
        """Test with all negative numbers."""
        # Mean = -3, deviations: |-1-(-3)|=2, |-2-(-3)|=1, |-3-(-3)|=0, |-4-(-3)|=1, |-5-(-3)|=2
        # MAD = (2+1+0+1+2)/5 = 1.2
        assert mean_absolute_deviation([-1.0, -2.0, -3.0, -4.0, -5.0]) == 1.2

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
        # Mean = 0, elements: -3, -1, 1, 3 => MAD = (3+1+1+3)/4 = 2.0
        assert mean_absolute_deviation([-3.0, -1.0, 1.0, 3.0]) == 2.0

    def test_float_values(self):
        """Test with non-integer float values."""
        # Mean = 2.5, deviations: |0.5-2.5|=2, |1.5-2.5|=1, |2.5-2.5|=0, |3.5-2.5|=1, |4.5-2.5|=2
        # MAD = (2+1+0+1+2)/5 = 1.2
        assert mean_absolute_deviation([0.5, 1.5, 2.5, 3.5, 4.5]) == 1.2

    def test_all_zeros(self):
        """All zero values should yield MAD of 0."""
        assert mean_absolute_deviation([0.0, 0.0, 0.0]) == 0.0

    def test_large_spread(self):
        """Test with widely spread values."""
        # Mean = 50, deviations: |0-50|=50, |25-50|=25, |50-50|=0, |75-50|=25, |100-50|=50
        # MAD = (50+25+0+25+50)/5 = 30.0
        assert mean_absolute_deviation([0.0, 25.0, 50.0, 75.0, 100.0]) == 30.0

    def test_two_different_elements(self):
        """Two different values: MAD = half their difference."""
        # Mean = 5, deviations: |0-5|=5, |10-5|=5 => MAD = 5.0
        assert mean_absolute_deviation([0.0, 10.0]) == 5.0

    def test_empty_list_raises_error(self):
        """Empty list should raise an error (division by zero)."""
        with pytest.raises(ZeroDivisionError):
            mean_absolute_deviation([])

    def test_non_numeric_input_raises_error(self):
        """Non-numeric input should raise TypeError."""
        with pytest.raises(TypeError):
            mean_absolute_deviation(["a", "b", "c"])
