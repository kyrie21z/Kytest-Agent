import pytest
from solution import rescale_to_unit


class TestRescaleToUnit:
    """Tests for the rescale_to_unit function."""

    def test_basic_positive_numbers(self):
        """Test with simple ascending positive numbers."""
        assert rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]

    def test_two_elements(self):
        """Test with exactly two elements (minimum required)."""
        assert rescale_to_unit([2.0, 4.0]) == [0.0, 1.0]

    def test_unsorted_input(self):
        """Test with unsorted input."""
        result = rescale_to_unit([5.0, 1.0, 3.0, 2.0, 4.0])
        assert result == [1.0, 0.0, 0.5, 0.25, 0.75]

    def test_negative_numbers(self):
        """Test with all negative numbers."""
        assert rescale_to_unit([-5.0, -4.0, -3.0, -2.0, -1.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]

    def test_mixed_positive_and_negative(self):
        """Test with mixed positive and negative numbers."""
        assert rescale_to_unit([-2.0, -1.0, 0.0, 1.0, 2.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]

    def test_duplicate_min_values(self):
        """Test when the minimum value appears multiple times."""
        assert rescale_to_unit([1.0, 1.0, 3.0, 5.0]) == [0.0, 0.0, 0.5, 1.0]

    def test_duplicate_max_values(self):
        """Test when the maximum value appears multiple times."""
        assert rescale_to_unit([1.0, 3.0, 5.0, 5.0]) == [0.0, 0.5, 1.0, 1.0]

    def test_all_same_values_raises_error(self):
        """Test that all identical values raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            rescale_to_unit([3.0, 3.0, 3.0])

    def test_single_element_at_start_becomes_zero(self):
        """Verify the smallest element always maps to 0.0."""
        result = rescale_to_unit([10.0, 20.0, 30.0])
        assert result[0] == 0.0

    def test_single_element_at_end_becomes_one(self):
        """Verify the largest element always maps to 1.0."""
        result = rescale_to_unit([10.0, 20.0, 30.0])
        assert result[-1] == 1.0

    def test_float_precision(self):
        """Test with non-integer floats."""
        result = rescale_to_unit([0.1, 0.3, 0.5])
        assert abs(result[0] - 0.0) < 1e-9
        assert abs(result[1] - 0.5) < 1e-9
        assert abs(result[2] - 1.0) < 1e-9

    def test_larger_range(self):
        """Test with a larger range of values."""
        result = rescale_to_unit([100.0, 200.0, 300.0, 400.0, 500.0])
        assert result == [0.0, 0.25, 0.5, 0.75, 1.0]

    def test_result_length_matches_input(self):
        """Ensure output list has the same length as input."""
        input_list = [1.0, 5.0, 3.0, 8.0, 2.0, 9.0, 4.0]
        result = rescale_to_unit(input_list)
        assert len(result) == len(input_list)

    def test_result_sum_property(self):
        """Test that the sum of rescaled values relates to the distribution."""
        # For evenly spaced values, the sum should be predictable
        result = rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
        assert sum(result) == pytest.approx(2.5)

    def test_descending_order_input(self):
        """Test with descending order input."""
        result = rescale_to_unit([5.0, 4.0, 3.0, 2.0, 1.0])
        assert result == [1.0, 0.75, 0.5, 0.25, 0.0]

    def test_three_elements(self):
        """Test with exactly three elements."""
        assert rescale_to_unit([10.0, 20.0, 30.0]) == [0.0, 0.5, 1.0]
