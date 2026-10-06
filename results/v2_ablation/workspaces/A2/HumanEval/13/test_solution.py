"""Unit tests for greatest_common_divisor in solution.py."""

import pytest
from solution import greatest_common_divisor


# ──────────────────────────────────────────────
# Normal / typical cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical positive integer inputs."""

    def test_coprime_numbers(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_one_divides_the_other(self):
        assert greatest_common_divisor(25, 15) == 5

    def test_multiple_of_each_other(self):
        assert greatest_common_divisor(10, 5) == 5

    def test_two_even_numbers(self):
        assert greatest_common_divisor(12, 8) == 4

    def test_larger_numbers(self):
        assert greatest_common_divisor(100, 75) == 25

    def test_prime_and_composite(self):
        assert greatest_common_divisor(7, 14) == 7

    def test_two_primes(self):
        assert greatest_common_divisor(11, 13) == 1

    def test_same_number(self):
        assert greatest_common_divisor(42, 42) == 42

    def test_order_independence(self):
        """GCD(a, b) == GCD(b, a)."""
        assert greatest_common_divisor(25, 15) == greatest_common_divisor(15, 25)


# ──────────────────────────────────────────────
# Boundary cases
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_one_with_itself(self):
        assert greatest_common_divisor(1, 1) == 1

    def test_one_with_large_number(self):
        assert greatest_common_divisor(1, 999999) == 1

    def test_large_number_with_one(self):
        assert greatest_common_divisor(999999, 1) == 1

    def test_zero_with_positive(self):
        """gcd(0, n) == n."""
        assert greatest_common_divisor(0, 7) == 7

    def test_positive_with_zero(self):
        """gcd(n, 0) == n."""
        assert greatest_common_divisor(7, 0) == 7

    def test_both_zeros(self):
        """gcd(0, 0) == 0."""
        assert greatest_common_divisor(0, 0) == 0

    def test_negative_first_argument(self):
        assert greatest_common_divisor(-25, 15) == 5

    def test_negative_second_argument(self):
        # Python's % keeps the sign of the divisor, so gcd(25, -15) → -5
        assert greatest_common_divisor(25, -15) == -5

    def test_both_negative(self):
        """When both are negative the implementation may return negative;
        document the actual behaviour here."""
        # With Python's % operator: gcd(-25, -15) → -5
        assert greatest_common_divisor(-25, -15) == -5

    def test_negative_first_only(self):
        assert greatest_common_divisor(-7, 7) == 7

    def test_large_inputs(self):
        assert greatest_common_divisor(10**9, 10**6) == 10**6

    def test_consecutive_integers(self):
        """Consecutive integers are coprime."""
        assert greatest_common_divisor(100, 101) == 1


# ──────────────────────────────────────────────
# Invalid-input / exception cases
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests that exercise invalid argument types."""

    @pytest.mark.parametrize("a, b", [
        ("hello", 5),
        (5, "world"),
        (None, 5),
        (5, None),
        ([5], 5),
        ({}, 5),
    ])
    def test_non_integer_types_raise_error(self, a, b):
        """Passing non-integers should raise an error (TypeError or ValueError)."""
        with pytest.raises((TypeError, ValueError)):
            greatest_common_divisor(a, b)

    @pytest.mark.parametrize("args", [
        (),           # no arguments
        (5,),         # only one argument
        (1, 2, 3),    # too many arguments
    ])
    def test_wrong_number_of_arguments_raises(self, args):
        """Calling with wrong number of positional arguments raises TypeError."""
        with pytest.raises(TypeError):
            greatest_common_divisor(*args)
