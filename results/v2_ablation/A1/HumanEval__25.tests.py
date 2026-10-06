"""Unit tests for solution.factorize."""

import pytest
from solution import factorize


class TestFactorizeNormalCases:
    """Tests with typical valid inputs."""

    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]

    def test_factorize_12(self):
        assert factorize(12) == [2, 2, 3]

    def test_factorize_6(self):
        assert factorize(6) == [2, 3]

    def test_factorize_100(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_factorize_30(self):
        assert factorize(30) == [2, 3, 5]

    def test_factorize_49(self):
        assert factorize(49) == [7, 7]

    def test_factorize_210(self):
        # 210 = 2 * 3 * 5 * 7
        assert factorize(210) == [2, 3, 5, 7]

    def test_factorize_16(self):
        assert factorize(16) == [2, 2, 2, 2]

    def test_factorize_27(self):
        assert factorize(27) == [3, 3, 3]

    def test_factorize_14(self):
        assert factorize(14) == [2, 7]

    def test_factorize_22(self):
        assert factorize(22) == [2, 11]

    def test_factorize_33(self):
        assert factorize(33) == [3, 11]

    def test_factorize_55(self):
        assert factorize(55) == [5, 11]

    def test_factorize_121(self):
        assert factorize(121) == [11, 11]

    def test_factorize_216(self):
        # 216 = 2^3 * 3^3
        assert factorize(216) == [2, 2, 2, 3, 3, 3]

    def test_factorize_1000(self):
        # 1000 = 2^3 * 5^3
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_factorize_2310(self):
        # 2310 = 2 * 3 * 5 * 7 * 11
        assert factorize(2310) == [2, 3, 5, 7, 11]


class TestFactorizeBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_factorize_1(self):
        # 1 has no prime factors
        assert factorize(1) == []

    def test_factorize_2(self):
        # Smallest prime number
        assert factorize(2) == [2]

    def test_factorize_3(self):
        # Second smallest prime
        assert factorize(3) == [3]

    def test_factorize_large_prime(self):
        # 97 is a prime number
        assert factorize(97) == [97]

    def test_factorize_larger_prime(self):
        # 101 is a prime number
        assert factorize(101) == [101]

    def test_factorize_prime_squared(self):
        # 169 = 13^2
        assert factorize(169) == [13, 13]

    def test_factorize_product_of_two_primes(self):
        # 143 = 11 * 13
        assert factorize(143) == [11, 13]

    def test_factorize_power_of_2(self):
        # 2^10 = 1024
        assert factorize(1024) == [2] * 10

    def test_factorize_power_of_3(self):
        # 3^5 = 243
        assert factorize(243) == [3] * 5

    def test_factorize_product_of_three_distinct_primes(self):
        # 2 * 13 * 17 = 442
        assert factorize(442) == [2, 13, 17]


class TestFactorizeProductProperty:
    """Verify that the product of returned factors equals the original number."""

    @pytest.mark.parametrize("n", [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 20, 24, 25, 27, 30, 36, 48, 49, 50, 64, 72,
        81, 100, 120, 128, 200, 256, 500, 1000, 2048, 4096,
    ])
    def test_product_equals_original(self, n):
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
                for i in range(len(factors) - 1):
                    assert factors[i] <= factors[i + 1]


class TestFactorizeEdgeCases:
    """Tests for zero and other edge-case inputs."""

    def test_factorize_zero(self):
        # 0 is not a valid input for prime factorization;
        # the implementation returns [] because sqrt(0)=0 and n=0 is not > 1.
        assert factorize(0) == []

    def test_factorize_one(self):
        # 1 has no prime factors
        assert factorize(1) == []


class TestFactorizeInvalidInputs:
    """Tests for invalid or unexpected inputs."""

    def test_negative_number_raises_valueerror(self):
        # math.sqrt(-1) raises ValueError
        with pytest.raises(ValueError):
            factorize(-1)

    def test_negative_two_raises_valueerror(self):
        with pytest.raises(ValueError):
            factorize(-10)

    def test_negative_large_raises_valueerror(self):
        with pytest.raises(ValueError):
            factorize(-1000)

    def test_string_input_raises_typeerror_or_valueerror(self):
        # Passing a string should fail when math.sqrt is called
        with pytest.raises((TypeError, ValueError)):
            factorize("8")

    def test_none_input_raises_typeerror(self):
        with pytest.raises(TypeError):
            factorize(None)

    def test_list_input_raises_typeerror(self):
        with pytest.raises(TypeError):
            factorize([2, 3])
