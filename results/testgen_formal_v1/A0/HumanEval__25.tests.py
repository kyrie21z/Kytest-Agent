import pytest
from solution import factorize


class TestFactorizeBasicCases:
    """Test basic cases documented in the docstring."""

    def test_factorize_8(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_25(self):
        assert factorize(25) == [5, 5]

    def test_factorize_70(self):
        assert factorize(70) == [2, 5, 7]


class TestFactorizeEdgeCases:
    """Test edge cases."""

    def test_factorize_one(self):
        """1 has no prime factors."""
        assert factorize(1) == []

    def test_factorize_two(self):
        """2 is the smallest prime."""
        assert factorize(2) == [2]

    def test_factorize_three(self):
        """3 is a prime."""
        assert factorize(3) == [3]

    def test_factorize_prime_number(self):
        """A prime number should return itself as the only factor."""
        assert factorize(13) == [13]

    def test_factorize_large_prime(self):
        """A larger prime number."""
        assert factorize(97) == [97]


class TestFactorizeCompositeNumbers:
    """Test various composite numbers."""

    def test_factorize_four(self):
        assert factorize(4) == [2, 2]

    def test_factorize_six(self):
        assert factorize(6) == [2, 3]

    def test_factorize_twelve(self):
        assert factorize(12) == [2, 2, 3]

    def test_factorize_thirty(self):
        assert factorize(30) == [2, 3, 5]

    def test_factorize_100(self):
        assert factorize(100) == [2, 2, 5, 5]

    def test_factorize_1000(self):
        assert factorize(1000) == [2, 2, 2, 5, 5, 5]

    def test_factorize_power_of_two(self):
        assert factorize(16) == [2, 2, 2, 2]

    def test_factorize_power_of_three(self):
        assert factorize(27) == [3, 3, 3]

    def test_factorize_perfect_square(self):
        assert factorize(49) == [7, 7]

    def test_factorize_product_of_two_primes(self):
        assert factorize(14) == [2, 7]

    def test_factorize_product_of_three_distinct_primes(self):
        assert factorize(30) == [2, 3, 5]

    def test_factorize_large_composite(self):
        assert factorize(1024) == [2] * 10

    def test_factorize_999999(self):
        assert factorize(999999) == [3, 3, 3, 7, 11, 13, 37]


class TestFactorizeProductProperty:
    """Verify that the product of returned factors equals the input."""

    @pytest.mark.parametrize("n", [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        12, 16, 25, 27, 30, 49, 50, 64,
        100, 128, 256, 512, 1000, 1024,
        999999, 1000000,
    ])
    def test_product_equals_input(self, n):
        factors = factorize(n)
        product = 1
        for f in factors:
            product *= f
        if n > 1:
            assert product == n
        else:
            # For n=1, empty factors means product stays 1
            assert product == 1


class TestFactorizeSortedOrder:
    """Verify that factors are returned in non-decreasing order."""

    @pytest.mark.parametrize("n", [
        2, 6, 12, 30, 100, 1000, 999999, 1000000,
    ])
    def test_factors_are_sorted(self, n):
        factors = factorize(n)
        assert factors == sorted(factors)


def _is_prime(num):
    """Helper function to check if a number is prime."""
    if num < 2:
        return False
    if num < 4:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


class TestFactorizeAllPrime:
    """Verify that every returned factor is actually prime."""

    @pytest.mark.parametrize("n", [
        2, 6, 12, 30, 100, 1000, 999999, 1000000,
    ])
    def test_all_factors_are_prime(self, n):
        factors = factorize(n)
        for f in factors:
            assert _is_prime(f), f"{f} is not prime"


class TestFactorizeReturnTypes:
    """Test that return types are correct."""

    def test_returns_list(self):
        result = factorize(8)
        assert isinstance(result, list)

    def test_empty_list_for_one(self):
        result = factorize(1)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_elements_are_integers(self):
        result = factorize(100)
        assert all(isinstance(x, int) for x in result)


class TestFactorizeDoctests:
    """Run doctests embedded in the function's docstring."""

    def test_doctests(self):
        import doctest
        import solution
        results = doctest.testmod(solution, verbose=False)
        assert results.failed == 0, f"{results.failed} doctest(s) failed"
