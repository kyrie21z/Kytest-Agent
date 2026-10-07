"""Unit tests for solution.greatest_common_divisor."""

import pytest
from solution import greatest_common_divisor


class TestGreatestCommonDivisor_NormalCases:
    """Tests with typical positive integer inputs."""

    def test_coprime_numbers(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_known_gcd_25_15(self):
        assert greatest_common_divisor(25, 15) == 5

    def test_gcd_12_8(self):
        assert greatest_common_divisor(12, 8) == 4

    def test_gcd_6_9(self):
        assert greatest_common_divisor(6, 9) == 3

    def test_gcd_100_75(self):
        assert greatest_common_divisor(100, 75) == 25

    def test_gcd_48_18(self):
        assert greatest_common_divisor(48, 18) == 6


class TestGreatestCommonDivisor_EqualNumbers:
    """Tests where both inputs are equal."""

    def test_equal_small(self):
        assert greatest_common_divisor(5, 5) == 5

    def test_equal_medium(self):
        assert greatest_common_divisor(100, 100) == 100

    def test_equal_large(self):
        assert greatest_common_divisor(9999, 9999) == 9999


class TestGreatestCommonDivisor_OneDividesOther:
    """Tests where one number evenly divides the other."""

    def test_smaller_divides_larger(self):
        assert greatest_common_divisor(4, 12) == 4

    def test_larger_divides_smaller(self):
        assert greatest_common_divisor(21, 7) == 7

    def test_one_and_any(self):
        """GCD(1, n) should always be 1."""
        assert greatest_common_divisor(1, 100) == 1
        assert greatest_common_divisor(100, 1) == 1


class TestGreatestCommonDivisor_PrimePairs:
    """Tests with prime numbers and coprime pairs."""

    def test_two_primes(self):
        assert greatest_common_divisor(2, 3) == 1

    def test_two_distinct_primes(self):
        assert greatest_common_divisor(17, 19) == 1

    def test_prime_and_multiple(self):
        assert greatest_common_divisor(7, 14) == 7


class TestGreatestCommonDivisor_ZeroHandling:
    """Tests involving zero as one or both inputs."""

    def test_first_is_zero(self):
        assert greatest_common_divisor(0, 5) == 5

    def test_second_is_zero(self):
        assert greatest_common_divisor(5, 0) == 5

    def test_both_are_zero(self):
        # GCD(0, 0) is mathematically undefined; the implementation returns 0
        assert greatest_common_divisor(0, 0) == 0

    def test_zero_with_negative(self):
        assert greatest_common_divisor(0, -7) == -7

    def test_negative_with_zero(self):
        assert greatest_common_divisor(-7, 0) == -7


class TestGreatestCommonDivisor_NegativeNumbers:
    """Tests with negative integer inputs.

    Tracing the Euclidean algorithm with Python's modulo semantics:
    - gcd(-5, 10): query_gcd(-5, 10) -> query_gcd(10, -5%10=5) -> query_gcd(5, 0) -> 5
    - gcd(5, -10): query_gcd(5, -10) -> query_gcd(-10, 5%-10=-5) -> query_gcd(-5, -10%-5=0) -> -5
    - gcd(-5, -10): query_gcd(-5, -10) -> query_gcd(-10, -5%-10=-5) -> query_gcd(-5, -10%-5=0) -> -5
    - gcd(7, -7): query_gcd(7, -7) -> query_gcd(-7, 7%-7=0) -> -7
    """

    def test_first_negative(self):
        result = greatest_common_divisor(-5, 10)
        assert result == 5

    def test_second_negative(self):
        result = greatest_common_divisor(5, -10)
        assert result == -5

    def test_both_negative(self):
        result = greatest_common_divisor(-5, -10)
        assert result == -5

    def test_same_magnitude_opposite_sign(self):
        result = greatest_common_divisor(7, -7)
        assert result == -7


class TestGreatestCommonDivisor_LargeNumbers:
    """Tests with large integer inputs."""

    def test_large_multiples(self):
        assert greatest_common_divisor(1000000, 500000) == 500000

    def test_large_coprime(self):
        assert greatest_common_divisor(1000003, 1000000) == 1

    def test_large_equal(self):
        assert greatest_common_divisor(999999, 999999) == 999999

    def test_power_of_two(self):
        assert greatest_common_divisor(1024, 512) == 512


class TestGreatestCommonDivisor_Commutativity:
    """Tests that GCD is commutative: gcd(a, b) == gcd(b, a)."""

    def test_commutative_pairs(self):
        pairs = [(3, 5), (25, 15), (12, 8), (48, 18), (100, 75)]
        for a, b in pairs:
            assert greatest_common_divisor(a, b) == greatest_common_divisor(b, a)


class TestGreatestCommonDivisor_DocstringExamples:
    """Verify the examples from the docstring pass exactly."""

    def test_docstring_example_1(self):
        assert greatest_common_divisor(3, 5) == 1

    def test_docstring_example_2(self):
        assert greatest_common_divisor(25, 15) == 5
