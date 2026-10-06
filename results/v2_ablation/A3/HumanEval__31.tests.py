"""Unit tests for solution.is_prime."""

import pytest
from solution import is_prime


# ---------------------------------------------------------------------------
# Normal / typical inputs – primes
# ---------------------------------------------------------------------------

class TestPrimes:
    """Tests where the expected result is True (the number IS prime)."""

    def test_two(self):
        """2 is the smallest prime."""
        assert is_prime(2) is True

    def test_three(self):
        """3 is prime."""
        assert is_prime(3) is True

    def test_five(self):
        """5 is prime."""
        assert is_prime(5) is True

    def test_seven(self):
        """7 is prime."""
        assert is_prime(7) is True

    def test_eleven(self):
        """11 is prime (also in docstring)."""
        assert is_prime(11) is True

    def test_sixty_one(self):
        """61 is prime (also in docstring)."""
        assert is_prime(61) is True

    def test_hundred_and_one(self):
        """101 is prime (also in docstring)."""
        assert is_prime(101) is True

    def test_large_prime_13441(self):
        """13441 is prime (also in docstring)."""
        assert is_prime(13441) is True

    def test_larger_prime_997(self):
        """997 is the largest 3-digit prime."""
        assert is_prime(997) is True

    def test_prime_104729(self):
        """104729 is the 10000th prime."""
        assert is_prime(104729) is True


# ---------------------------------------------------------------------------
# Normal / typical inputs – composites
# ---------------------------------------------------------------------------

class TestComposites:
    """Tests where the expected result is False (the number is NOT prime)."""

    def test_four(self):
        """4 = 2 × 2 (also in docstring)."""
        assert is_prime(4) is False

    def test_six(self):
        """6 = 2 × 3 (also in docstring)."""
        assert is_prime(6) is False

    def test_nine(self):
        """9 = 3 × 3."""
        assert is_prime(9) is False

    def test_fifteen(self):
        """15 = 3 × 5."""
        assert is_prime(15) is False

    def test_eighteen(self):
        """18 = 2 × 9."""
        assert is_prime(18) is False

    def test_even_composite_100(self):
        """100 is even and composite."""
        assert is_prime(100) is False

    def test_odd_composite_25(self):
        """25 = 5 × 5."""
        assert is_prime(25) is False

    def test_odd_composite_35(self):
        """35 = 5 × 7."""
        assert is_prime(35) is False

    def test_square_of_prime_49(self):
        """49 = 7 × 7."""
        assert is_prime(49) is False

    def test_product_of_two_primes_143(self):
        """143 = 11 × 13."""
        assert is_prime(143) is False


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaries:
    """Edge-of-range inputs."""

    def test_zero(self):
        """0 is not prime."""
        assert is_prime(0) is False

    def test_one(self):
        """1 is not prime (also in docstring)."""
        assert is_prime(1) is False

    def test_negative_one(self):
        """-1 is not prime."""
        assert is_prime(-1) is False

    def test_negative_ten(self):
        """-10 is not prime."""
        assert is_prime(-10) is False

    def test_negative_100(self):
        """-100 is not prime."""
        assert is_prime(-100) is False

    def test_two_boundary(self):
        """2 is the boundary between non-prime and prime."""
        assert is_prime(2) is True

    def test_three_boundary(self):
        """3 is the next prime after 2."""
        assert is_prime(3) is True


# ---------------------------------------------------------------------------
# Large-number stress tests
# ---------------------------------------------------------------------------

class TestLargeNumbers:
    """Stress tests with larger values."""

    def test_large_prime_104729(self):
        """104729 is the 10000th prime."""
        assert is_prime(104729) is True

    def test_large_composite_100000(self):
        """100000 is clearly composite."""
        assert is_prime(100000) is False

    def test_large_prime_100003(self):
        """100003 is prime."""
        assert is_prime(100003) is True

    def test_perfect_square_10000(self):
        """10000 = 100² is composite."""
        assert is_prime(10000) is False

    def test_power_of_two_1024(self):
        """1024 = 2¹⁰ is composite."""
        assert is_prime(1024) is False


# ---------------------------------------------------------------------------
# Docstring doctest examples (explicit re-check)
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    """Re-verify every example shown in the docstring."""

    @pytest.mark.parametrize("n, expected", [
        (6,   False),
        (101, True),
        (11,  True),
        (13441, True),
        (61,  True),
        (4,   False),
        (1,   False),
    ])
    def test_docstring_examples(self, n, expected):
        """Every example from the docstring must match."""
        assert is_prime(n) == expected
