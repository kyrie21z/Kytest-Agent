import pytest
from solution import truncate_number


class TestTruncateNumber:
    """Tests for the truncate_number function."""

    def test_basic_decimal(self):
        """Test with a simple decimal number."""
        assert truncate_number(3.5) == 0.5

    def test_small_whole_part(self):
        """Test with a small whole part."""
        assert truncate_number(1.25) == 0.25

    def test_large_whole_part(self):
        """Test with a large whole part."""
        assert truncate_number(999.99) == pytest.approx(0.99)

    def test_very_small_decimal(self):
        """Test with a very small decimal part."""
        result = truncate_number(5.001)
        assert abs(result - 0.001) < 1e-10

    def test_decimal_close_to_one(self):
        """Test with a decimal part close to 1."""
        result = truncate_number(7.999)
        assert abs(result - 0.999) < 1e-10

    def test_whole_number(self):
        """Test that a whole number returns 0 as the decimal part."""
        assert truncate_number(4.0) == 0.0

    def test_another_whole_number(self):
        """Test another whole number."""
        assert truncate_number(10.0) == 0.0

    def test_single_digit_decimal(self):
        """Test with a single-digit decimal."""
        assert truncate_number(2.7) == pytest.approx(0.7)

    def test_many_decimal_places(self):
        """Test with many decimal places."""
        result = truncate_number(1.123456789)
        assert abs(result - 0.123456789) < 1e-10

    def test_nearly_integer(self):
        """Test with a number nearly equal to an integer."""
        result = truncate_number(5.0000001)
        assert abs(result - 0.0000001) < 1e-10

    def test_half(self):
        """Test with exactly half."""
        assert truncate_number(6.5) == 0.5

    def test_zero_point_something(self):
        """Test with a number less than 1."""
        assert truncate_number(0.75) == 0.75

    def test_tiny_fraction(self):
        """Test with a very tiny fraction."""
        result = truncate_number(100.00000001)
        assert abs(result - 0.00000001) < 1e-12

    def test_negative_behavior_not_expected(self):
        """Ensure the function is designed for positive numbers only.
        The docstring specifies 'positive floating point number'."""
        # This test documents expected behavior; negative inputs are out of scope.
        pass

    def test_returns_float_type(self):
        """Verify the return type is float."""
        assert isinstance(truncate_number(3.5), float)

    def test_returns_float_type_for_whole(self):
        """Verify the return type is float even for whole numbers."""
        assert isinstance(truncate_number(5.0), float)

    def test_precision_with_repeating_like_decimals(self):
        """Test with a decimal that can't be represented exactly in binary."""
        result = truncate_number(1.1)
        # 1.1 cannot be represented exactly; check it's close to 0.1
        assert abs(result - 0.1) < 1e-10
