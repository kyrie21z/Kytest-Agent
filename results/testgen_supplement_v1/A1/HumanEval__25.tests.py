"""Unit tests for solution.factorize."""

import pytest
from solution import factorize


class TestFactorizeDocstringExamples:
    """Tests from the docstring examples."""

    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]


class TestFactorizeNormalCases:
    """Tests with typical positive integer inputs."""

    def test_factorize_2(self):
        """Smallest prime number."""
        assert factorize(2) == [2]

    def test_factorize_3(self):
        """Another small prime."""
        assert factorize(3) == [3]

    def test_factorize_6(self):
        """Product of two distinct primes."""
        assert factorize(6) == [2, 3]

    def test_factorize_12(self):
        """Small composite with repeated factors."""
        assert factorize(12) == [2, 2, 3]

    def test_factorize_100(self):
        """Larger composite with multiple repeated factors."""
        assert factorize(100) == [2, 2, 5, 5]

    def test_factorize_1000(self):
        """Three repeated factors of two different primes."""
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_factorize_49(self):
        """Square of a prime."""
        assert factorize(49) == [7, 7]

    def test_factorize_27(self):
        """Cube of a prime."""
        assert factorize(27) == [3, 3, 3]

    def test_factorize_210(self):
        """Product of first four primes: 2 * 3 * 5 * 7."""
        assert factorize(210) == [2, 3, 5, 7]

    def test_factorize_1024(self):
        """Power of 2: 2^10."""
        assert factorize(1024) == [2] * 10

    def test_factorize_36(self):
        """6 squared: 2^2 * 3^2."""
        assert factorize(36) == [2, 2, 3, 3]

    def test_factorize_large_prime_product(self):
        """Product of two large primes: 101 * 103 = 10403."""
        assert factorize(10403) == [101, 103]


class TestFactorizeBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_factorize_1(self):
        """1 has no prime factors; product of empty list is 1."""
        assert factorize(1) == []

    def test_factorize_4(self):
        """Smallest square of a prime."""
        assert factorize(4) == [2, 2]

    def test_factorize_9(self):
        """Square of 3."""
        assert factorize(9) == [3, 3]

    def test_factorize_16(self):
        """Power of 2: 2^4."""
        assert factorize(16) == [2, 2, 2, 2]

    def test_factorize_81(self):
        """Power of 3: 3^4."""
        assert factorize(81) == [3, 3, 3, 3]

    def test_factorize_2147483647(self):
        """Largest known Mersenne prime (2^31 - 1)."""
        assert factorize(2147483647) == [2147483647]

    def test_factorize_2147483646(self):
        """One less than largest Mersenne prime: 2 * 3^2 * 7 * 11 * 31 * 151 * 331."""
        assert factorize(2147483646) == [2, 3, 3, 7, 11, 31, 151, 331]


class TestFactorizeProperties:
    """Tests verifying mathematical properties of factorize output."""

    @staticmethod
    def _product_of_list(lst):
        result = 1
        for x in lst:
            result *= x
        return result

    def test_product_equals_original(self):
        """The product of all factors must equal the original number."""
        for n in range(2, 1000):
            factors = factorize(n)
            assert self._product_of_list(factors) == n

    def test_factors_are_sorted(self):
        """Factors must be in non-decreasing order."""
        for n in range(2, 1000):
            factors = factorize(n)
            assert factors == sorted(factors)

    def test_all_factors_are_prime(self):
        """Every factor returned must be a prime number."""
        def is_prime(x):
            if x < 2:
                return False
            if x == 2:
                return True
            if x % 2 == 0:
                return False
            for i in range(3, int(x**0.5) + 1, 2):
                if x % i == 0:
                    return False
            return True

        for n in range(2, 1000):
            factors = factorize(n)
            for f in factors:
                assert is_prime(f), f"{f} is not prime"

    def test_empty_for_one(self):
        """factorize(1) returns empty list, and product of empty list is 1."""
        assert factorize(1) == []


class TestFactorizeInvalidInputs:
    """Tests for invalid inputs that should raise exceptions."""

    def test_factorize_zero(self):
        """Zero is not a valid input for prime factorization."""
        # math.sqrt(0) = 0, loop condition 2 <= 1 is False, n=0, n > 1 is False
        # Returns [] but this is arguably incorrect behavior for an invalid input.
        # We document the actual behavior.
        assert factorize(0) == []

    def test_factorize_negative(self):
        """Negative numbers cause math.sqrt to raise ValueError."""
        with pytest.raises(ValueError):
            factorize(-1)

    def test_factorize_negative_five(self):
        """Another negative number also raises ValueError."""
        with pytest.raises(ValueError):
            factorize(-5)

    def test_factorize_negative_large(self):
        """Large negative number also raises ValueError."""
        with pytest.raises(ValueError):
            factorize(-1000)
