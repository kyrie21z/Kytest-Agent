"""Unit tests for is_prime function in solution.py."""
import pytest
from solution import is_prime


# ---- Docstring examples ----

class TestDocstringExamples:
    def test_is_prime_6(self):
        assert is_prime(6) is False

    def test_is_prime_101(self):
        assert is_prime(101) is True

    def test_is_prime_11(self):
        assert is_prime(11) is True

    def test_is_prime_13441(self):
        assert is_prime(13441) is True

    def test_is_prime_61(self):
        assert is_prime(61) is True

    def test_is_prime_4(self):
        assert is_prime(4) is False

    def test_is_prime_1(self):
        assert is_prime(1) is False


# ---- Edge cases ----

class TestEdgeCases:
    def test_negative_numbers(self):
        assert is_prime(-1) is False
        assert is_prime(-5) is False
        assert is_prime(-100) is False

    def test_zero(self):
        assert is_prime(0) is False

    def test_one(self):
        assert is_prime(1) is False

    def test_two(self):
        assert is_prime(2) is True

    def test_three(self):
        assert is_prime(3) is True


# ---- Known primes ----

class TestKnownPrimes:
    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
    def test_small_primes(self, n):
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [97, 101, 103, 107, 109])
    def test_near_hundred_primes(self, n):
        assert is_prime(n) is True

    def test_larger_prime(self):
        assert is_prime(997) is True


# ---- Known composites ----

class TestKnownComposites:
    @pytest.mark.parametrize("n", [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    def test_small_composites(self, n):
        assert is_prime(n) is False

    def test_even_composite(self):
        assert is_prime(100) is False

    def test_odd_composite(self):
        assert is_prime(9) is False
        assert is_prime(25) is False
        assert is_prime(49) is False

    def test_square_of_prime(self):
        assert is_prime(49) is False   # 7^2
        assert is_prime(121) is False  # 11^2


# ---- Type and return value checks ----

class TestReturnTypes:
    def test_returns_bool(self):
        result = is_prime(7)
        assert isinstance(result, bool)

    def test_returns_false_for_non_prime(self):
        assert is_prime(4) is False

    def test_returns_true_for_prime(self):
        assert is_prime(7) is True
