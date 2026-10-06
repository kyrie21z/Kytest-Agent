import pytest
from solution import largest_prime_factor


# ---------------------------------------------------------------------------
# Docstring doctest examples
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    """Cases taken directly from the function's docstring."""

    def test_13195(self):
        # 13195 = 5 × 7 × 13 × 29
        assert largest_prime_factor(13195) == 29

    def test_2048(self):
        # 2048 = 2^11
        assert largest_prime_factor(2048) == 2


# ---------------------------------------------------------------------------
# Normal cases – typical composite inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Typical composite numbers with distinct prime factors."""

    def test_6(self):
        # 6 = 2 × 3
        assert largest_prime_factor(6) == 3

    def test_10(self):
        # 10 = 2 × 5
        assert largest_prime_factor(10) == 5

    def test_15(self):
        # 15 = 3 × 5
        assert largest_prime_factor(15) == 5

    def test_14(self):
        # 14 = 2 × 7
        assert largest_prime_factor(14) == 7

    def test_21(self):
        # 21 = 3 × 7
        assert largest_prime_factor(21) == 7

    def test_77(self):
        # 77 = 7 × 11
        assert largest_prime_factor(77) == 11

    def test_35(self):
        # 35 = 5 × 7
        assert largest_prime_factor(35) == 7

    def test_55(self):
        # 55 = 5 × 11
        assert largest_prime_factor(55) == 11

    def test_143(self):
        # 143 = 11 × 13
        assert largest_prime_factor(143) == 13


# ---------------------------------------------------------------------------
# Boundary cases – edges of the valid input range
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Smallest / simplest valid inputs and products of two primes."""

    def test_4(self):
        # 4 = 2^2 — smallest composite > 1
        assert largest_prime_factor(4) == 2

    def test_9(self):
        # 9 = 3^2
        assert largest_prime_factor(9) == 3

    def test_25(self):
        # 25 = 5^2
        assert largest_prime_factor(25) == 5

    def test_12(self):
        # 12 = 2^2 × 3
        assert largest_prime_factor(12) == 3

    def test_18(self):
        # 18 = 2 × 3^2
        assert largest_prime_factor(18) == 3

    def test_50(self):
        # 50 = 2 × 5^2
        assert largest_prime_factor(50) == 5

    def test_100(self):
        # 100 = 2^2 × 5^2
        assert largest_prime_factor(100) == 5


# ---------------------------------------------------------------------------
# Larger-number cases
# ---------------------------------------------------------------------------

class TestLargerNumbers:
    """Inputs with more digits to exercise the sieve at scale."""

    def test_1000000(self):
        # 1000000 = 2^6 × 5^6
        assert largest_prime_factor(1000000) == 5

    def test_999999(self):
        # 999999 = 3^3 × 7 × 11 × 13 × 37
        assert largest_prime_factor(999999) == 37

    def test_1000001(self):
        # 1000001 = 101 × 9901
        assert largest_prime_factor(1000001) == 9901

    def test_1000002(self):
        # 1000002 = 2 × 3 × 166667
        assert largest_prime_factor(1000002) == 166667


# ---------------------------------------------------------------------------
# Invalid inputs – outside documented preconditions
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Inputs that violate the docstring precondition (n > 1, n not prime)."""

    def test_n_equals_1(self):
        # n = 1 has no prime factors; function returns None.
        assert largest_prime_factor(1) is None

    def test_n_equals_0(self):
        # n = 0: sieve array tiny, no divisor found.
        assert largest_prime_factor(0) is None

    def test_negative_n(self):
        # Negative n: sieve array tiny, no divisor found.
        assert largest_prime_factor(-5) is None

    def test_prime_input(self):
        # Primes are excluded by the docstring, but the function still runs.
        # For a prime p, the only divisor checked is 1 (isprime[1] is True),
        # so it returns 1.
        assert largest_prime_factor(7) == 1
        assert largest_prime_factor(13) == 1
        assert largest_prime_factor(97) == 1


# ---------------------------------------------------------------------------
# Additional edge: product of two large primes
# ---------------------------------------------------------------------------

class TestProductOfTwoPrimes:
    """Composites that are exactly the product of two primes."""

    def test_2_times_3(self):
        assert largest_prime_factor(6) == 3

    def test_2_times_large_prime(self):
        # 2 × 997 = 1994
        assert largest_prime_factor(1994) == 997

    def test_3_times_101(self):
        # 3 × 101 = 303
        assert largest_prime_factor(303) == 101

    def test_13_times_17(self):
        # 13 × 17 = 221
        assert largest_prime_factor(221) == 17
