import pytest
from solution import poly, find_zero


class TestPoly:
    """Tests for the poly function."""

    def test_constant_polynomial(self):
        """Test evaluating a constant polynomial (single coefficient)."""
        assert poly([5], 10) == 5

    def test_linear_polynomial(self):
        """Test f(x) = 1 + 2x at x = 3 => 7."""
        assert poly([1, 2], 3) == 7

    def test_quadratic_polynomial(self):
        """Test f(x) = 1 + 2x + 3x^2 at x = 2 => 1 + 4 + 12 = 17."""
        assert poly([1, 2, 3], 2) == 17

    def test_cubic_polynomial(self):
        """Test f(x) = 1 + 2x + 3x^2 + 4x^3 at x = 1 => 1+2+3+4 = 10."""
        assert poly([1, 2, 3, 4], 1) == 10

    def test_at_zero(self):
        """Any polynomial evaluated at x=0 returns the constant term."""
        assert poly([3, 5, 7, 9], 0) == 3

    def test_negative_x(self):
        """Test with negative x value: f(-1) = 1 - 2 + 3 - 4 = -2."""
        assert poly([1, 2, 3, 4], -1) == -2

    def test_float_coefficients(self):
        """Test with floating point coefficients."""
        result = poly([0.5, 1.5], 2)
        assert result == pytest.approx(3.5)

    def test_float_x(self):
        """Test with float x value."""
        result = poly([1, 2], 0.5)
        assert result == pytest.approx(2.0)

    def test_higher_degree_polynomial(self):
        """Test a degree-4 polynomial at x=1 => sum of all coeffs."""
        coeffs = [1, 2, 3, 4, 5]
        assert poly(coeffs, 1) == sum(coeffs)

    def test_single_coefficient_nonzero_x(self):
        """Constant polynomial should return same value regardless of x."""
        assert poly([7], 100) == 7
        assert poly([7], -50) == 7


class TestFindZero:
    """Tests for the find_zero function."""

    def test_simple_linear(self):
        """f(x) = 1 + 2x => zero at x = -0.5."""
        assert round(find_zero([1, 2]), 2) == -0.5

    def test_cubic_with_known_roots(self):
        """f(x) = (x-1)(x-2)(x-3) = -6 + 11x - 6x^2 + x^3 => root at 1.0."""
        assert round(find_zero([-6, 11, -6, 1]), 2) == 1.0

    def test_docstring_example_1(self):
        """Verify docstring example: round(find_zero([1, 2]), 2) == -0.5."""
        assert round(find_zero([1, 2]), 2) == -0.5

    def test_docstring_example_2(self):
        """Verify docstring example: round(find_zero([-6, 11, -6, 1]), 2) == 1.0."""
        assert round(find_zero([-6, 11, -6, 1]), 2) == 1.0

    def test_linear_with_negative_constant(self):
        """f(x) = -4 + 2x => zero at x = 2."""
        assert round(find_zero([-4, 2]), 2) == 2.0

    def test_linear_with_positive_slope_and_constant(self):
        """f(x) = 3 + 6x => zero at x = -0.5."""
        assert round(find_zero([3, 6]), 2) == -0.5

    def test_quartic_polynomial(self):
        """Test with 6 coefficients (degree 5 polynomial)."""
        # f(x) = 1 - 2x + ... ; we just check it returns a reasonable number
        result = find_zero([1, -2, 1, 0, 0, 0])
        assert isinstance(result, float)

    def test_large_coefficients(self):
        """Test with large coefficient values."""
        result = round(find_zero([1000, 2000]), 2)
        assert result == -0.5

    def test_mixed_sign_coefficients(self):
        """Test with alternating sign coefficients."""
        result = round(find_zero([1, -1, 1, -1]), 2)
        assert isinstance(result, float)

    def test_returns_float(self):
        """find_zero should always return a float."""
        result = find_zero([1, 2])
        assert isinstance(result, float)

    def test_near_zero_result(self):
        """Test a polynomial where the root is near 0."""
        # f(x) = 0.001 + x => root at x = -0.001
        result = round(find_zero([0.001, 1]), 4)
        assert result == -0.001

    def test_even_number_of_coefficients(self):
        """find_zero requires an even number of coefficients per docstring."""
        # This test documents expected behavior; the function may or may not
        # raise on odd-length lists. We test with valid even-length inputs.
        result = find_zero([2, 4, -3, -1])
        assert isinstance(result, float)

    def test_precision_check(self):
        """Verify that the result is accurate to within tolerance."""
        # f(x) = 1 + 2x has exact root -0.5
        result = find_zero([1, 2])
        assert abs(result - (-0.5)) < 1e-4

    def test_cubic_root_accuracy(self):
        """Check accuracy of cubic polynomial root finding."""
        result = find_zero([-6, 11, -6, 1])
        # One root is exactly 1.0
        assert abs(result - 1.0) < 1e-4
