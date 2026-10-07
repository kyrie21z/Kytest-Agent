"""Unit tests for largest_prime_factor."""

import pytest
from solution import largest_prime_factor


class TestLargestPrimeFactorDocstringExamples:
    """Tests from the docstring examples."""

    def test_13195(self):
        assert largest_prime_factor(13195) == 29

    def test_2048(self):
        assert largest_prime_factor(2048) == 2


class TestLargestPrimeFactorNormalCases:
    """Tests with typical composite inputs."""

    def test_small_composite_4(self):
        # 4 = 2 * 2, largest prime factor is 2
        assert largest_prime_factor(4) == 2

    def test_small_composite_6(self):
        # 6 = 2 * 3, largest prime factor is 3
        assert largest_prime_factor(6) == 3

    def test_small_composite_9(self):
        # 9 = 3 * 3, largest prime factor is 3
        assert largest_prime_factor(9) == 3

    def test_small_composite_10(self):
        # 10 = 2 * 5, largest prime factor is 5
        assert largest_prime_factor(10) == 5

    def test_small_composite_14(self):
        # 14 = 2 * 7, largest prime factor is 7
        assert largest_prime_factor(14) == 7

    def test_small_composite_15(self):
        # 15 = 3 * 5, largest prime factor is 5
        assert largest_prime_factor(15) == 5

    def test_small_composite_21(self):
        # 21 = 3 * 7, largest prime factor is 7
        assert largest_prime_factor(21) == 7

    def test_small_composite_35(self):
        # 35 = 5 * 7, largest prime factor is 7
        assert largest_prime_factor(35) == 7

    def test_100(self):
        # 100 = 2^2 * 5^2, largest prime factor is 5
        assert largest_prime_factor(100) == 5

    def test_1000(self):
        # 1000 = 2^3 * 5^3, largest prime factor is 5
        assert largest_prime_factor(1000) == 5

    def test_77(self):
        # 77 = 7 * 11, largest prime factor is 11
        assert largest_prime_factor(77) == 11

    def test_143(self):
        # 143 = 11 * 13, largest prime factor is 13
        assert largest_prime_factor(143) == 13

    def test_323(self):
        # 323 = 17 * 19, largest prime factor is 19
        assert largest_prime_factor(323) == 19

    def test_power_of_two(self):
        # 2^10 = 1024, only prime factor is 2
        assert largest_prime_factor(1024) == 2

    def test_power_of_three(self):
        # 3^5 = 243, only prime factor is 3
        assert largest_prime_factor(243) == 3

    def test_product_of_two_primes(self):
        # 2 * 97 = 194, largest prime factor is 97
        assert largest_prime_factor(194) == 97

    def test_product_of_two_larger_primes(self):
        # 13 * 17 = 221, largest prime factor is 17
        assert largest_prime_factor(221) == 17

    def test_even_number_with_large_prime_factor(self):
        # 2 * 47 = 94, largest prime factor is 47
        assert largest_prime_factor(94) == 47

    def test_odd_number_with_distinct_prime_factors(self):
        # 3 * 5 * 7 = 105, largest prime factor is 7
        assert largest_prime_factor(105) == 7

    def test_multiple_same_prime_factors(self):
        # 2^3 * 3^2 = 72, largest prime factor is 3
        assert largest_prime_factor(72) == 3


class TestLargestPrimeFactorBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_valid_input(self):
        # Smallest composite number per docstring (n > 1, not prime)
        assert largest_prime_factor(4) == 2

    def test_square_of_prime(self):
        # 11^2 = 121, largest prime factor is 11
        assert largest_prime_factor(121) == 11

    def test_cube_of_prime(self):
        # 5^3 = 125, largest prime factor is 5
        assert largest_prime_factor(125) == 5

    def test_fourth_power_of_prime(self):
        # 2^4 = 16, largest prime factor is 2
        assert largest_prime_factor(16) == 2

    def test_highly_composite_number(self):
        # 210 = 2 * 3 * 5 * 7, largest prime factor is 7
        assert largest_prime_factor(210) == 7

    def test_larger_number(self):
        # 9999 = 3^2 * 11 * 101, largest prime factor is 101
        assert largest_prime_factor(9999) == 101

    def test_number_with_single_large_prime_factor(self):
        # 2 * 997 = 1994, largest prime factor is 997
        assert largest_prime_factor(1994) == 997


class TestLargestPrimeFactorInvalidInputs:
    """Tests with inputs outside the documented contract."""

    def test_n_equals_one(self):
        # Docstring says n > 1; n=1 is outside the contract
        # No proper prime factor exists, returns None
        assert largest_prime_factor(1) is None

    def test_n_equals_zero(self):
        # Docstring says n > 1; n=0 is outside the contract
        assert largest_prime_factor(0) is None

    def test_negative_number(self):
        # Docstring says n > 1; negative values are outside the contract
        # Creates empty list, no factors found, returns None
        assert largest_prime_factor(-5) is None

    def test_prime_number(self):
        # Docstring says n is not a prime; primes are outside the contract
        # isprime[1] remains True and n % 1 == 0, so returns 1
        assert largest_prime_factor(7) == 1

    def test_another_prime(self):
        assert largest_prime_factor(13) == 1

    def test_large_prime(self):
        assert largest_prime_factor(97) == 1


class TestLargestPrimeFactorEdgeValues:
    """Additional edge case tests."""

    def test_two_times_prime(self):
        # 2 * 3 = 6
        assert largest_prime_factor(6) == 3

    def test_three_times_prime(self):
        # 3 * 11 = 33
        assert largest_prime_factor(33) == 11

    def test_five_times_prime(self):
        # 5 * 13 = 65
        assert largest_prime_factor(65) == 13

    def test_eight(self):
        # 8 = 2^3
        assert largest_prime_factor(8) == 2

    def test_twelve(self):
        # 12 = 2^2 * 3
        assert largest_prime_factor(12) == 3

    def test_thirty(self):
        # 30 = 2 * 3 * 5
        assert largest_prime_factor(30) == 5

    def test_sixty(self):
        # 60 = 2^2 * 3 * 5
        assert largest_prime_factor(60) == 5

    def test_hundred_and_twenty(self):
        # 120 = 2^3 * 3 * 5
        assert largest_prime_factor(120) == 5
