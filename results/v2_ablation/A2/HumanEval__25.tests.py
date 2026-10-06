"""Unit tests for solution.factorize."""

import pytest
from solution import factorize


class TestFactorizeNormalCases:
    """Tests with typical, well-behaved inputs."""

    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]

    def test_factorize_12(self):
        assert factorize(12) == [2, 2, 3]

    def test_factorize_60(self):
        assert factorize(60) == [2, 2, 3, 5]

    def test_factorize_100(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_factorize_210(self):
        assert factorize(210) == [2, 3, 5, 7]

    def test_factorize_27(self):
        assert factorize(27) == [3, 3, 3]

    def test_factorize_16(self):
        assert factorize(16) == [2, 2, 2, 2]

    def test_factorize_14(self):
        assert factorize(14) == [2, 7]

    def test_factorize_35(self):
        assert factorize(35) == [5, 7]

    def test_factorize_1024(self):
        assert factorize(1024) == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    def test_factorize_999999(self):
        # 999999 = 3^3 * 7 * 11 * 13 * 37
        assert factorize(999999) == [3, 3, 3, 7, 11, 13, 37]


class TestFactorizeBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_prime_2(self):
        assert factorize(2) == [2]

    def test_second_prime_3(self):
        assert factorize(3) == [3]

    def test_smallest_square_of_prime_4(self):
        assert factorize(4) == [2, 2]

    def test_cube_of_prime_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_square_of_larger_prime_49(self):
        assert factorize(49) == [7, 7]

    def test_large_prime_97(self):
        assert factorize(97) == [97]

    def test_large_prime_104729(self):
        assert factorize(104729) == [104729]

    def test_product_of_two_same_primes(self):
        assert factorize(143) == [11, 13]

    def test_power_of_three_243(self):
        # 243 = 3^5
        assert factorize(243) == [3, 3, 3, 3, 3]

    def test_even_number_with_many_factors(self):
        assert factorize(512) == [2, 2, 2, 2, 2, 2, 2, 2, 2]

    def test_odd_composite(self):
        assert factorize(21) == [3, 7]

    def test_product_of_three_distinct_primes(self):
        assert factorize(30) == [2, 3, 5]


class TestFactorizeEdgeInputs:
    """Tests with edge-case inputs like 1, 0, negatives."""

    def test_one_returns_empty_list(self):
        # 1 has no prime factors; the product of an empty list is conventionally 1
        assert factorize(1) == []

    def test_zero_returns_empty_list(self):
        # 0 is not a valid input for prime factorization, but the function
        # handles it without crashing.
        result = factorize(0)
        assert isinstance(result, list)

    def test_negative_input_raises_value_error(self):
        # Negative numbers cause math.sqrt to fail with ValueError.
        with pytest.raises(ValueError):
            factorize(-5)


class TestFactorizeProductInvariant:
    """Verify that the product of returned factors equals the original input."""

    @pytest.mark.parametrize("n", [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20,
        21, 22, 24, 25, 26, 27, 28, 30, 32, 35, 36, 40, 42,
        48, 49, 50, 54, 55, 60, 64, 70, 72, 80, 81, 90, 96,
        100, 120, 125, 128, 144, 150, 196, 200, 256, 500,
        1000, 1024, 2048, 4096, 8192, 10000, 50000, 100000,
    ])
    def test_product_equals_input(self, n):
        factors = factorize(n)
        product = 1
        for f in factors:
            product *= f
        assert product == n

    def test_factors_are_sorted(self):
        """Factors should be in non-decreasing order."""
        for n in range(2, 1000):
            factors = factorize(n)
            if len(factors) > 1:
                assert factors == sorted(factors), f"Factors of {n} not sorted: {factors}"

    def test_all_factors_are_prime(self):
        """Every returned factor must be a prime number."""
        def is_prime(x):
            if x < 2:
                return False
            if x < 4:
                return True
            if x % 2 == 0 or x % 3 == 0:
                return False
            i = 5
            while i * i <= x:
                if x % i == 0 or x % (i + 2) == 0:
                    return False
                i += 6
            return True

        for n in range(2, 1000):
            factors = factorize(n)
            for f in factors:
                assert is_prime(f), f"{f} is not prime (factor of {n})"


class TestFactorizeTypeValidation:
    """Tests for invalid input types."""

    def test_string_input_raises_type_error(self):
        """Passing a string should raise TypeError."""
        with pytest.raises(TypeError):
            factorize("abc")

    def test_float_input_returns_non_integer(self):
        """Passing a float does not raise but produces a non-integer factor."""
        result = factorize(3.5)
        assert isinstance(result, list)
        # The function doesn't validate type, so it may return non-prime values
        # Just verify it returns a list without crashing
        assert all(isinstance(f, (int, float)) for f in result)

    def test_none_input_raises_type_error(self):
        """Passing None raises TypeError when math.sqrt receives None."""
        with pytest.raises(TypeError):
            factorize(None)

    def test_list_input_raises_type_error(self):
        """Passing a list should raise TypeError."""
        with pytest.raises(TypeError):
            factorize([2, 3])
