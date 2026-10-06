"""Unit tests for solution.largest_prime_factor."""

import pytest
from solution import largest_prime_factor


class TestDocstringExamples:
    """Tests from the function's docstring."""

    def test_13195(self):
        assert largest_prime_factor(13195) == 29

    def test_2048(self):
        assert largest_prime_factor(2048) == 2


class TestNormalCases:
    """Typical composite inputs with known expected results."""

    def test_smallest_composite_4(self):
        # 4 = 2^2, largest prime factor is 2
        assert largest_prime_factor(4) == 2

    def test_6(self):
        # 6 = 2 * 3, largest prime factor is 3
        assert largest_prime_factor(6) == 3

    def test_15(self):
        # 15 = 3 * 5, largest prime factor is 5
        assert largest_prime_factor(15) == 5

    def test_21(self):
        # 21 = 3 * 7, largest prime factor is 7
        assert largest_prime_factor(21) == 7

    def test_100(self):
        # 100 = 2^2 * 5^2, largest prime factor is 5
        assert largest_prime_factor(100) == 5

    def test_77(self):
        # 77 = 7 * 11, largest prime factor is 11
        assert largest_prime_factor(77) == 11

    def test_12(self):
        # 12 = 2^2 * 3, largest prime factor is 3
        assert largest_prime_factor(12) == 3

    def test_35(self):
        # 35 = 5 * 7, largest prime factor is 7
        assert largest_prime_factor(35) == 7

    def test_49(self):
        # 49 = 7^2, largest prime factor is 7
        assert largest_prime_factor(49) == 7

    def test_27(self):
        # 27 = 3^3, largest prime factor is 3
        assert largest_prime_factor(27) == 3

    def test_143(self):
        # 143 = 11 * 13, largest prime factor is 13
        assert largest_prime_factor(143) == 13

    def test_999(self):
        # 999 = 3^3 * 37, largest prime factor is 37
        assert largest_prime_factor(999) == 37

    def test_large_power_of_two(self):
        # 2^10 = 1024, largest prime factor is 2
        assert largest_prime_factor(1024) == 2

    def test_product_of_distinct_primes(self):
        # 2 * 3 * 5 * 7 = 210, largest prime factor is 7
        assert largest_prime_factor(210) == 7

    def test_81(self):
        # 81 = 3^4, largest prime factor is 3
        assert largest_prime_factor(81) == 3

    def test_1024(self):
        # 1024 = 2^10, largest prime factor is 2
        assert largest_prime_factor(1024) == 2


class TestBoundaryCases:
    """Edge-of-valid-input-range cases."""

    def test_min_valid_composite_4(self):
        # The smallest composite number > 1
        assert largest_prime_factor(4) == 2

    def test_6(self):
        # Smallest composite with two distinct prime factors
        assert largest_prime_factor(6) == 3

    def test_even_composite(self):
        # Even composite where largest prime factor is odd
        assert largest_prime_factor(14) == 7

    def test_odd_composite(self):
        # Odd composite
        assert largest_prime_factor(9) == 3

    def test_square_of_prime(self):
        # Square of a prime: 13^2 = 169
        assert largest_prime_factor(169) == 13

    def test_cube_of_prime(self):
        # Cube of a prime: 5^3 = 125
        assert largest_prime_factor(125) == 5


class TestInvalidInputs:
    """Inputs that violate the documented assumptions (n > 1, n not prime).

    The function does not validate its preconditions. For inputs outside
    the documented range, it falls through without returning a value,
    which means it returns None. For prime inputs, it returns 1 because
    isprime[1] is True and n % 1 == 0.
    """

    @pytest.mark.parametrize("n", [1, 0, -1, -10])
    def test_n_leq_one_returns_none(self, n):
        """n <= 1 violates the assumption n > 1.
        
        The function creates a list of size n+1 and searches for a
        prime factor < n. For n <= 1, no such factor exists, so
        the function returns None.
        """
        assert largest_prime_factor(n) is None

    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23])
    def test_prime_input_returns_one(self, n):
        """Prime numbers violate the assumption that n is not prime.
        
        For a prime n, the sieve marks all non-primes as False, but
        n itself is prime. The loop checks n-1 down to 1, and since
        isprime[1] is True and n % 1 == 0, the function returns 1.
        """
        assert largest_prime_factor(n) == 1


class TestReturnType:
    """Verify return types are correct."""

    def test_returns_int(self):
        result = largest_prime_factor(15)
        assert isinstance(result, int)

    def test_returns_positive_int(self):
        result = largest_prime_factor(15)
        assert result > 0
