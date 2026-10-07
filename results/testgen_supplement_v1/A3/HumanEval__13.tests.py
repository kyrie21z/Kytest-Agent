"""Unit tests for solution.greatest_common_divisor."""

import pytest
from solution import greatest_common_divisor


class TestGCD_NormalCases:
    """Tests with typical positive integer inputs."""

    def test_coprime_numbers(self):
        """GCD of two coprime numbers is 1."""
        assert greatest_common_divisor(3, 5) == 1

    def test_one_divides_the_other(self):
        """When one number divides the other, GCD is the smaller number."""
        assert greatest_common_divisor(25, 15) == 5
        assert greatest_common_divisor(15, 25) == 5

    def test_prime_and_multiple(self):
        """GCD of a prime and its multiple is the prime."""
        assert greatest_common_divisor(7, 21) == 7
        assert greatest_common_divisor(21, 7) == 7

    def test_both_same_prime(self):
        """GCD of a prime with itself is the prime."""
        assert greatest_common_divisor(7, 7) == 7

    def test_larger_pair(self):
        """GCD of larger typical numbers."""
        assert greatest_common_divisor(100, 75) == 25

    def test_even_numbers(self):
        """GCD of even numbers."""
        assert greatest_common_divisor(12, 18) == 6
        assert greatest_common_divisor(48, 36) == 12

    def test_power_of_two(self):
        """GCD involving powers of two."""
        assert greatest_common_divisor(8, 16) == 8
        assert greatest_common_divisor(16, 8) == 8


class TestGCD_BoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_first_input_zero(self):
        """GCD(0, b) returns b."""
        assert greatest_common_divisor(0, 5) == 5

    def test_second_input_zero(self):
        """GCD(a, 0) returns a."""
        assert greatest_common_divisor(5, 0) == 5

    def test_both_inputs_zero(self):
        """GCD(0, 0) returns 0."""
        assert greatest_common_divisor(0, 0) == 0

    def test_equal_nonzero(self):
        """GCD(a, a) returns a."""
        assert greatest_common_divisor(10, 10) == 10
        assert greatest_common_divisor(100, 100) == 100

    def test_negative_first_positive_second(self):
        """GCD with a negative first argument and positive second."""
        # query_gcd(-12, 8) -> query_gcd(8, -12 % 8) = query_gcd(8, 4) -> query_gcd(4, 0) -> 4
        assert greatest_common_divisor(-12, 8) == 4

    def test_positive_first_negative_second(self):
        """GCD with a positive first argument and negative second."""
        # query_gcd(12, -8) -> query_gcd(-8, 12 % -8) = query_gcd(-8, -4) -> query_gcd(-4, 0) -> -4
        assert greatest_common_divisor(12, -8) == -4

    def test_both_negative(self):
        """GCD with both arguments negative."""
        # query_gcd(-12, -8) -> query_gcd(-8, -12 % -8) = query_gcd(-8, -4) -> query_gcd(-4, 0) -> -4
        assert greatest_common_divisor(-12, -8) == -4

    def test_one_is_one(self):
        """GCD with 1 as one argument (coprime to everything)."""
        assert greatest_common_divisor(1, 100) == 1
        assert greatest_common_divisor(100, 1) == 1

    def test_one_is_minus_one(self):
        """GCD with -1 as one argument."""
        # gcd(-1, 5): query_gcd(-1, 5) -> query_gcd(5, -1 % 5) = query_gcd(5, 4) -> ... -> 1
        assert greatest_common_divisor(-1, 5) == 1
        # gcd(5, -1): query_gcd(5, -1) -> query_gcd(-1, 5 % -1) = query_gcd(-1, 0) -> -1
        assert greatest_common_divisor(5, -1) == -1

    def test_large_numbers(self):
        """GCD with large integers."""
        assert greatest_common_divisor(1000000, 500000) == 500000
        assert greatest_common_divisor(999999, 1000000) == 1


class TestGCD_Commutativity:
    """Tests verifying GCD(a, b) == GCD(b, a) for cases where it holds."""

    @pytest.mark.parametrize("a, b", [
        (3, 5),
        (25, 15),
        (12, 18),
        (100, 75),
        (7, 21),
        (48, 36),
    ])
    def test_commutativity_positive(self, a, b):
        """GCD is commutative for positive inputs: gcd(a, b) == gcd(b, a)."""
        assert greatest_common_divisor(a, b) == greatest_common_divisor(b, a)

    def test_negative_order_breaks_commutativity(self):
        """Demonstrate that commutativity does not hold for mixed-sign negatives."""
        # gcd(-12, 8) = 4 but gcd(8, -12) = -4
        assert greatest_common_divisor(-12, 8) != greatest_common_divisor(8, -12)

    def test_positive_first_negative_second_breaks_commutativity(self):
        """gcd(12, -8) = -4 but gcd(-8, 12) = 4."""
        assert greatest_common_divisor(12, -8) != greatest_common_divisor(-8, 12)


class TestGCD_InvalidInputs:
    """Tests for invalid input types that may raise exceptions."""

    @pytest.mark.parametrize("invalid_a, invalid_b", [
        ("hello", 5),
        (5, "world"),
        ("abc", "def"),
        ([1, 2], 5),
        (None, 5),
        ({}, 5),
    ])
    def test_invalid_types_raise_error(self, invalid_a, invalid_b):
        """Passing non-integer types should raise an exception."""
        with pytest.raises(Exception):
            greatest_common_divisor(invalid_a, invalid_b)

    def test_float_inputs_do_not_raise(self):
        """Float inputs are accepted by the function (Python allows float modulo)."""
        # These don't raise; they compute using float arithmetic
        result = greatest_common_divisor(3.0, 5.0)
        assert isinstance(result, float)


class TestGCD_DocstringExamples:
    """Verify the exact examples from the docstring."""

    def test_docstring_example_1(self):
        """>>> greatest_common_divisor(3, 5) -> 1"""
        assert greatest_common_divisor(3, 5) == 1

    def test_docstring_example_2(self):
        """>>> greatest_common_divisor(25, 15) -> 5"""
        assert greatest_common_divisor(25, 15) == 5
