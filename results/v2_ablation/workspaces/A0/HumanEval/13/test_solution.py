"""Unit tests for solution.greatest_common_divisor."""

import pytest
from solution import greatest_common_divisor


class TestGreatestCommonDivisorBasic:
    """Test basic functionality with positive integers."""

    def test_coprime_numbers(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_non_trivial_gcd(self):
        assert greatest_common_divisor(25, 15) == 5

    def test_one_divides_other(self):
        assert greatest_common_divisor(10, 5) == 5

    def test_same_number(self):
        assert greatest_common_divisor(7, 7) == 7

    def test_order_independence(self):
        assert greatest_common_divisor(15, 25) == 5
        assert greatest_common_divisor(25, 15) == 5

    def test_larger_first(self):
        assert greatest_common_divisor(100, 25) == 25

    def test_smaller_first(self):
        assert greatest_common_divisor(25, 100) == 25


class TestGreatestCommonDivisorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_one_is_zero(self):
        assert greatest_common_divisor(0, 5) == 5

    def test_other_is_zero(self):
        assert greatest_common_divisor(5, 0) == 5

    def test_both_are_zero(self):
        assert greatest_common_divisor(0, 0) == 0

    def test_one(self):
        assert greatest_common_divisor(1, 1) == 1

    def test_one_with_large_number(self):
        assert greatest_common_divisor(1, 100) == 1
        assert greatest_common_divisor(100, 1) == 1


class TestGreatestCommonDivisorNegativeNumbers:
    """Test behavior with negative numbers (implementation does not abs values)."""

    def test_negative_second(self):
        # The recursive Euclidean algorithm preserves sign of the last non-zero remainder
        assert greatest_common_divisor(10, -5) == -5

    def test_negative_first(self):
        assert greatest_common_divisor(-10, 5) == 5

    def test_both_negative(self):
        assert greatest_common_divisor(-10, -5) == -5

    def test_negative_coprime(self):
        assert greatest_common_divisor(-3, 5) == 1


class TestGreatestCommonDivisorLargeNumbers:
    """Test with larger integer values."""

    def test_large_primes(self):
        assert greatest_common_divisor(104729, 104743) == 1

    def test_large_composite(self):
        assert greatest_common_divisor(1000000, 500000) == 500000

    def test_two_large_equal(self):
        assert greatest_common_divisor(999999, 999999) == 999999

    def test_fibonacci_like_sequence(self):
        # Consecutive Fibonacci numbers are coprime
        assert greatest_common_divisor(6765, 4181) == 1


class TestGreatestCommonDivisorPrimeNumbers:
    """Test with prime numbers."""

    def test_two_different_primes(self):
        assert greatest_common_divisor(7, 13) == 1

    def test_prime_and_multiple(self):
        assert greatest_common_divisor(7, 21) == 7

    def test_same_prime(self):
        assert greatest_common_divisor(11, 11) == 11


class TestGreatestCommonDivisorTypeChecking:
    """Test that the function handles expected input types."""

    def test_integer_input(self):
        assert isinstance(greatest_common_divisor(12, 8), int)

    def test_return_type_for_zero(self):
        assert isinstance(greatest_common_divisor(0, 0), int)
