"""Unit tests for solution.greatest_common_divisor."""

import pytest
from solution import greatest_common_divisor


# ---------------------------------------------------------------------------
# Normal / typical cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical positive integer inputs."""

    def test_coprime_primes(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_one_divides_other(self):
        assert greatest_common_divisor(25, 15) == 5

    def test_even_numbers(self):
        assert greatest_common_divisor(12, 8) == 4

    def test_larger_coprime(self):
        assert greatest_common_divisor(17, 13) == 1

    def test_both_same(self):
        assert greatest_common_divisor(9, 9) == 9

    def test_one_is_one(self):
        assert greatest_common_divisor(1, 100) == 1

    def test_other_is_one(self):
        assert greatest_common_divisor(100, 1) == 1

    def test_large_multiple(self):
        assert greatest_common_divisor(1_000_000, 500_000) == 500_000

    def test_order_independence(self):
        """GCD is commutative: gcd(a, b) == gcd(b, a)."""
        assert greatest_common_divisor(25, 15) == greatest_common_divisor(15, 25)

    def test_negative_result_consistency(self):
        """gcd(100, 75) == gcd(75, 100) == 25."""
        assert greatest_common_divisor(100, 75) == 25


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of the input domain."""

    def test_zero_first_argument(self):
        """gcd(a, 0) == a."""
        assert greatest_common_divisor(5, 0) == 5

    def test_zero_second_argument(self):
        """gcd(0, b) == b."""
        assert greatest_common_divisor(0, 7) == 7

    def test_both_zero(self):
        """gcd(0, 0) == 0."""
        assert greatest_common_divisor(0, 0) == 0

    def test_one_and_zero(self):
        assert greatest_common_divisor(1, 0) == 1

    def test_zero_and_one(self):
        assert greatest_common_divisor(0, 1) == 1

    def test_negative_first(self):
        """GCD with a negative first argument; result carries sign of b."""
        # query_gcd(-4, 6) -> query_gcd(6, -4%6=2) -> query_gcd(2, 6%2=0) -> 2
        assert greatest_common_divisor(-4, 6) == 2

    def test_negative_second(self):
        """GCD with a negative second argument; result carries sign of b."""
        # query_gcd(4, -6) -> query_gcd(-6, 4%-6=4) -> query_gcd(4, -6%4=-2)
        #   -> query_gcd(-2, 4%-2=0) -> -2
        assert greatest_common_divisor(4, -6) == -2

    def test_both_negative(self):
        """GCD with both arguments negative."""
        # query_gcd(-3, -5) -> query_gcd(-5, -3%-5=-3) -> query_gcd(-3, -5%-3=-2)
        #   -> query_gcd(-2, -3%-2=-1) -> query_gcd(-1, -2%-1=0) -> -1
        assert greatest_common_divisor(-3, -5) == -1

    def test_negative_coprime(self):
        assert greatest_common_divisor(-7, 11) == 1

    def test_negative_one_divides_other(self):
        assert greatest_common_divisor(-12, 8) == 4


# ---------------------------------------------------------------------------
# Empty / null / zero-size inputs
# ---------------------------------------------------------------------------

class TestEdgeInputs:
    """Tests involving zero, one, and identity-like values."""

    def test_identity_element(self):
        """gcd(n, 1) == 1 for any n > 0."""
        assert greatest_common_divisor(42, 1) == 1

    def test_single_digit(self):
        assert greatest_common_divisor(2, 3) == 1

    def test_two_digit(self):
        assert greatest_common_divisor(11, 22) == 11

    def test_three_digit(self):
        assert greatest_common_divisor(100, 200) == 100


# ---------------------------------------------------------------------------
# Invalid inputs – type checking
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests for inputs outside the documented int type."""

    @pytest.mark.parametrize("a, b", [
        ("3", 5),
        (3, "5"),
        ([3], [5]),
        ({}, {}),
        (None, 5),
        (3, None),
    ])
    def test_non_integer_raises(self, a, b):
        """Non-integer types should raise TypeError."""
        with pytest.raises(TypeError):
            greatest_common_divisor(a, b)

    @pytest.mark.parametrize("a, b", [
        (3.5, 5),
        (3, 5.0),
    ])
    def test_float_inputs_accepted(self, a, b):
        """Float inputs are accepted by the implementation (no type guard)."""
        # The recursive % operator works on floats in Python.
        result = greatest_common_divisor(a, b)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# Doctest-style verification against docstring examples
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    """Reproduce every example from the docstring."""

    def test_docstring_example_1(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_docstring_example_2(self):
        assert greatest_common_divisor(25, 15) == 5
