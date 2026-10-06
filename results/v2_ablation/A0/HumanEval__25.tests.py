import pytest
from solution import factorize


class TestFactorize:
    """Tests for the factorize function."""

    def test_factorize_small_prime(self):
        assert factorize(2) == [2]

    def test_factorize_two(self):
        assert factorize(2) == [2]

    def test_factorize_three(self):
        assert factorize(3) == [3]

    def test_factorize_four(self):
        assert factorize(4) == [2, 2]

    def test_factorize_eight(self):
        assert factorize(8) == [2, 2, 2]

    def test_factorize_twenty_five(self):
        assert factorize(25) == [5, 5]

    def test_factorize_seventy(self):
        assert factorize(70) == [2, 5, 7]

    def test_factorize_even_number(self):
        assert factorize(14) == [2, 7]

    def test_factorize_odd_composite(self):
        assert factorize(9) == [3, 3]

    def test_factorize_product_of_factors(self):
        """Verify that the product of all factors equals the original number."""
        for n in range(2, 100):
            factors = factorize(n)
            product = 1
            for f in factors:
                product *= f
            assert product == n

    def test_factorize_large_prime(self):
        assert factorize(97) == [97]

    def test_factorize_square_of_prime(self):
        assert factorize(49) == [7, 7]

    def test_factorize_cube_of_prime(self):
        assert factorize(27) == [3, 3, 3]

    def test_factorize_returns_list(self):
        result = factorize(12)
        assert isinstance(result, list)

    def test_factorize_sorted_order(self):
        """Factors should be in non-decreasing order."""
        for n in range(2, 200):
            factors = factorize(n)
            assert factors == sorted(factors)
