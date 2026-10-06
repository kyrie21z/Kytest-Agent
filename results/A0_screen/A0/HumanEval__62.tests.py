import pytest
from solution import derivative


class TestDerivative:
    """Tests for the derivative function."""

    # ---- Docstring examples ----

    def test_docstring_example_1(self):
        """Polynomial 3 + x + 2x^2 + 4x^3 + 5x^4 -> derivative 1 + 4x + 12x^2 + 20x^3"""
        assert derivative([3, 1, 2, 4, 5]) == [1, 4, 12, 20]

    def test_docstring_example_2(self):
        """Polynomial 1 + 2x + 3x^2 -> derivative 2 + 6x"""
        assert derivative([1, 2, 3]) == [2, 6]

    # ---- Edge cases ----

    def test_empty_list(self):
        """Derivative of an empty polynomial should be empty."""
        assert derivative([]) == []

    def test_single_constant(self):
        """Derivative of a constant (single coefficient) is zero-length."""
        assert derivative([5]) == []

    def test_two_elements_linear(self):
        """Derivative of ax + b is just a."""
        assert derivative([7, 3]) == [3]

    # ---- Simple polynomials ----

    def test_quadratic(self):
        """Derivative of 4 + 2x + 5x^2 is 2 + 10x."""
        assert derivative([4, 2, 5]) == [2, 10]

    def test_cubic(self):
        """Derivative of 1 + 0x + 3x^2 + 2x^3 is 0 + 6x + 6x^2."""
        assert derivative([1, 0, 3, 2]) == [0, 6, 6]

    def test_zero_polynomial(self):
        """Derivative of all zeros is all zeros."""
        assert derivative([0, 0, 0, 0]) == [0, 0, 0]

    # ---- Negative and mixed coefficients ----

    def test_negative_coefficients(self):
        """Derivative with negative coefficients."""
        assert derivative([-1, -2, -3]) == [-2, -6]

    def test_mixed_signs(self):
        """Derivative with mixed positive and negative coefficients."""
        assert derivative([5, -3, 2, -1]) == [-3, 4, -3]

    # ---- Larger polynomials ----

    def test_higher_degree(self):
        """Derivative of a degree-5 polynomial."""
        xs = [0, 1, 0, 0, 0, 1]  # x + x^5
        assert derivative(xs) == [1, 0, 0, 0, 5]

    def test_all_zeros_except_last(self):
        """Only the highest-degree term is non-zero."""
        assert derivative([0, 0, 0, 0, 7]) == [0, 0, 0, 28]

    # ---- Coefficient magnitude ----

    def test_large_coefficients(self):
        """Derivative handles large integer coefficients."""
        assert derivative([1000000, 2000000, 3000000]) == [2000000, 6000000]

    def test_fractional_like_via_integers(self):
        """Coefficients that produce varied results after multiplication."""
        assert derivative([0, 1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]

    # ---- Type / structure checks ----

    def test_returns_list(self):
        """Ensure the result is a list."""
        assert isinstance(derivative([1, 2]), list)

    def test_result_length(self):
        """Result length should be len(xs) - 1."""
        for n in range(1, 10):
            xs = list(range(n))
            result = derivative(xs)
            assert len(result) == max(0, n - 1)
