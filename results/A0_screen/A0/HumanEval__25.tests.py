import pytest
from solution import factorize


class TestFactorizeBasic:
    """Test basic cases documented in the docstring."""

    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]


class TestFactorizeEdgeCases:
    """Test edge cases."""

    def test_factorize_prime(self):
        """A prime number should return itself as the only factor."""
        assert factorize(7) == [7]

    def test_factorize_2(self):
        """Smallest prime."""
        assert factorize(2) == [2]

    def test_factorize_3(self):
        """Another small prime."""
        assert factorize(3) == [3]

    def test_factorize_1(self):
        """1 has no prime factors."""
        assert factorize(1) == []

    def test_factorize_negative_raises(self):
        """Negative numbers raise ValueError due to math.sqrt domain error."""
        with pytest.raises(ValueError):
            factorize(-5)

    def test_factorize_zero(self):
        """Zero has no meaningful prime factorization."""
        result = factorize(0)
        assert isinstance(result, list)


class TestFactorizeProductProperty:
    """Verify that the product of returned factors equals the original number."""

    @pytest.mark.parametrize("n", [
        4, 6, 9, 10, 12, 14, 15, 16, 18, 20,
        21, 22, 24, 27, 28, 30, 32, 36, 40, 42,
        48, 49, 50, 54, 55, 60, 64, 72, 80, 100,
        128, 256, 512, 1000, 1024, 2048, 4096,
        8191, 10000, 65536, 100000, 999999,
    ])
    def test_product_of_factors_equals_n(self, n):
        if n <= 1:
            return  # Skip n=1 (empty product) and negatives
        factors = factorize(n)
        product = 1
        for f in factors:
            product *= f
        assert product == n


class TestFactorizeSortedOrder:
    """Verify that factors are returned in non-decreasing order."""

    @pytest.mark.parametrize("n", [
        2, 4, 6, 8, 12, 30, 100, 1000, 10000, 999999,
    ])
    def test_factors_are_sorted(self, n):
        factors = factorize(n)
        assert factors == sorted(factors)


class TestFactorizeAllPrimes:
    """Verify that every returned factor is indeed a prime number."""

    def _is_prime(self, num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    @pytest.mark.parametrize("n", [
        2, 4, 6, 8, 12, 30, 100, 1000, 10000, 999999,
    ])
    def test_all_factors_are_prime(self, n):
        factors = factorize(n)
        for f in factors:
            assert self._is_prime(f), f"{f} is not prime"


class TestFactorizeSpecificValues:
    """Additional specific test values."""

    def test_factorize_4(self):
        assert factorize(4) == [2, 2]

    def test_factorize_6(self):
        assert factorize(6) == [2, 3]

    def test_factorize_12(self):
        assert factorize(12) == [2, 2, 3]

    def test_factorize_100(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_factorize_1000(self):
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_factorize_large_prime(self):
        """8191 is a known Mersenne prime (2^13 - 1)."""
        assert factorize(8191) == [8191]

    def test_factorize_power_of_two(self):
        assert factorize(1024) == [2] * 10

    def test_factorize_square_of_prime(self):
        assert factorize(49) == [7, 7]

    def test_factorize_cube_of_prime(self):
        assert factorize(27) == [3, 3, 3]
