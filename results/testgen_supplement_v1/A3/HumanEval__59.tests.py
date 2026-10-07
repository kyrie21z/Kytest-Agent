"""Unit tests for largest_prime_factor in solution.py."""

import pytest
from solution import largest_prime_factor


class TestDocstringExamples:
    """Test cases explicitly given in the docstring."""

    def test_13195(self):
        assert largest_prime_factor(13195) == 29

    def test_2048(self):
        assert largest_prime_factor(2048) == 2


class TestNormalCases:
    """Typical composite inputs with known largest prime factors."""

    def test_4(self):
        # 4 = 2^2, largest prime factor is 2
        assert largest_prime_factor(4) == 2

    def test_6(self):
        # 6 = 2 * 3, largest prime factor is 3
        assert largest_prime_factor(6) == 3

    def test_8(self):
        # 8 = 2^3, largest prime factor is 2
        assert largest_prime_factor(8) == 2

    def test_9(self):
        # 9 = 3^2, largest prime factor is 3
        assert largest_prime_factor(9) == 3

    def test_10(self):
        # 10 = 2 * 5, largest prime factor is 5
        assert largest_prime_factor(10) == 5

    def test_15(self):
        # 15 = 3 * 5, largest prime factor is 5
        assert largest_prime_factor(15) == 5

    def test_21(self):
        # 21 = 3 * 7, largest prime factor is 7
        assert largest_prime_factor(21) == 7

    def test_100(self):
        # 100 = 2^2 * 5^2, largest prime factor is 5
        assert largest_prime_factor(100) == 5

    def test_105(self):
        # 105 = 3 * 5 * 7, largest prime factor is 7
        assert largest_prime_factor(105) == 7

    def test_143(self):
        # 143 = 11 * 13, largest prime factor is 13
        assert largest_prime_factor(143) == 13

    def test_323(self):
        # 323 = 17 * 19, largest prime factor is 19
        assert largest_prime_factor(323) == 19

    def test_600(self):
        # 600 = 2^3 * 3 * 5^2, largest prime factor is 5
        assert largest_prime_factor(600) == 5

    def test_power_of_two(self):
        # 2^10 = 1024, only prime factor is 2
        assert largest_prime_factor(1024) == 2

    def test_product_of_two_primes(self):
        # 2 * 97 = 194, largest prime factor is 97
        assert largest_prime_factor(194) == 97

    def test_larger_composite(self):
        # 999999 = 3 * 3 * 3 * 7 * 11 * 13 * 37
        # Largest prime factor is 37
        assert largest_prime_factor(999999) == 37

    def test_even_with_odd_factors(self):
        # 2 * 3 * 5 * 7 * 11 * 13 = 30030
        # Largest prime factor is 13
        assert largest_prime_factor(30030) == 13


class TestBoundaryCases:
    """Edge-of-valid-range inputs."""

    def test_smallest_composite(self):
        # 4 is the smallest composite number (>1 and not prime)
        assert largest_prime_factor(4) == 2

    def test_even_number_with_small_factors(self):
        # 12 = 2^2 * 3, largest prime factor is 3
        assert largest_prime_factor(12) == 3

    def test_odd_composite(self):
        # 27 = 3^3, largest prime factor is 3
        assert largest_prime_factor(27) == 3

    def test_square_of_prime(self):
        # 49 = 7^2, largest prime factor is 7
        assert largest_prime_factor(49) == 7

    def test_cube_of_prime(self):
        # 125 = 5^3, largest prime factor is 5
        assert largest_prime_factor(125) == 5

    def test_product_of_same_prime(self):
        # 8 = 2^3, largest prime factor is 2
        assert largest_prime_factor(8) == 2

    def test_three_distinct_primes(self):
        # 2 * 3 * 5 = 30, largest prime factor is 5
        assert largest_prime_factor(30) == 5


class TestInvalidInputs:
    """Inputs outside documented constraints (n > 1, not prime)."""

    def test_n_equals_1(self):
        # Docstring assumes n > 1; n=1 has no prime factors
        result = largest_prime_factor(1)
        assert result is None

    def test_n_equals_0(self):
        # n=0 is outside documented constraint
        result = largest_prime_factor(0)
        assert result is None

    def test_negative_input(self):
        # Negative n is outside documented constraint
        result = largest_prime_factor(-5)
        assert result is None

    def test_n_equals_2(self):
        # 2 is prime, not composite — violates "not a prime" assumption
        result = largest_prime_factor(2)
        assert result == 1

    def test_n_equals_3(self):
        # 3 is prime, not composite
        result = largest_prime_factor(3)
        assert result == 1

    def test_n_equals_5(self):
        # 5 is prime
        result = largest_prime_factor(5)
        assert result == 1

    def test_n_equals_7(self):
        # 7 is prime
        result = largest_prime_factor(7)
        assert result == 1


class TestNonIntegerInputs:
    """Inputs that are not integers."""

    def test_float_input(self):
        # Passing a float may produce unexpected behavior
        with pytest.raises(TypeError):
            largest_prime_factor(15.0)

    def test_string_input(self):
        with pytest.raises(TypeError):
            largest_prime_factor("15")

    def test_none_input(self):
        with pytest.raises(TypeError):
            largest_prime_factor(None)
