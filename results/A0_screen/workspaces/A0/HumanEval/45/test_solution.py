"""Unit tests for solution.triangle_area."""

import pytest
from solution import triangle_area


class TestTriangleArea:
    """Tests for the triangle_area function."""

    # --- Positive integer inputs ---

    def test_basic_example(self):
        """Test the doctest example: base=5, height=3 -> area=7.5"""
        assert triangle_area(5, 3) == 7.5

    def test_equal_base_and_height(self):
        """Base and height are equal."""
        assert triangle_area(4, 4) == 8.0

    def test_unit_values(self):
        """Both inputs are 1."""
        assert triangle_area(1, 1) == 0.5

    def test_large_values(self):
        """Large integer inputs."""
        assert triangle_area(100, 200) == 10000.0

    def test_one_side_is_one(self):
        """One side is 1, other is larger."""
        assert triangle_area(1, 10) == 5.0
        assert triangle_area(10, 1) == 5.0

    # --- Float inputs ---

    def test_float_inputs(self):
        """Both inputs are floats."""
        assert triangle_area(2.5, 4.0) == 5.0

    def test_fractional_inputs(self):
        """Fractional base and height."""
        assert triangle_area(0.5, 0.5) == 0.125

    def test_mixed_int_float(self):
        """One int, one float."""
        assert triangle_area(6, 2.5) == 7.5

    # --- Zero inputs ---

    def test_zero_base(self):
        """Base is zero; area should be zero."""
        assert triangle_area(0, 5) == 0.0

    def test_zero_height(self):
        """Height is zero; area should be zero."""
        assert triangle_area(5, 0) == 0.0

    def test_both_zero(self):
        """Both base and height are zero."""
        assert triangle_area(0, 0) == 0.0

    # --- Negative inputs ---

    def test_negative_base(self):
        """Negative base produces negative area (formula-based behavior)."""
        assert triangle_area(-5, 3) == -7.5

    def test_negative_height(self):
        """Negative height produces negative area (formula-based behavior)."""
        assert triangle_area(5, -3) == -7.5

    def test_both_negative(self):
        """Both negative yields positive area (negative × negative = positive)."""
        assert triangle_area(-5, -3) == 7.5

    # --- Precision checks ---

    def test_precision_with_repeating_decimal(self):
        """Ensure floating-point precision with repeating decimals."""
        result = triangle_area(1, 3)
        assert abs(result - 1.5) < 1e-9

    def test_precision_small_numbers(self):
        """Small decimal inputs."""
        result = triangle_area(0.1, 0.2)
        assert abs(result - 0.01) < 1e-9

    # --- Return type checks ---

    def test_returns_float_for_integer_inputs(self):
        """Even with integer inputs, the result should be a float."""
        assert isinstance(triangle_area(2, 4), float)

    def test_returns_float_for_float_inputs(self):
        """With float inputs, result should also be float."""
        assert isinstance(triangle_area(2.0, 4.0), float)

    # --- Boundary / edge cases ---

    def test_very_small_positive(self):
        """Very small positive values."""
        result = triangle_area(1e-10, 1e-10)
        assert result == pytest.approx(5e-21)

    def test_very_large_values(self):
        """Very large values near typical float limits."""
        result = triangle_area(1e15, 1e15)
        assert result == pytest.approx(5e29)
