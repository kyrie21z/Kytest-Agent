"""Unit tests for is_multiply_prime in solution.py.

The function returns True if the given number is the product of exactly
3 prime numbers (counting multiplicity), and False otherwise.
Per the docstring, a < 100.
"""

import pytest
from solution import is_multiply_prime


# ---------------------------------------------------------------------------
# Normal / typical cases – products of exactly 3 primes
# ---------------------------------------------------------------------------

class TestNormalCasesProductOfThreePrimes:
    """Inputs that ARE the product of exactly 3 primes → True."""

    @pytest.mark.parametrize("a, factors", [
        (8, "2*2*2"),
        (12, "2*2*3"),
        (18, "2*3*3"),
        (20, "2*2*5"),
        (28, "2*2*7"),
        (44, "2*2*11"),
        (45, "3*3*5"),
        (50, "2*5*5"),
        (52, "2*2*13"),
        (63, "3*3*7"),
        (68, "2*2*17"),
        (75, "3*5*5"),
        (76, "2*2*19"),
        (92, "2*2*23"),
        (98, "2*7*7"),
        (99, "3*3*11"),
    ])
    def test_product_of_three_primes(self, a, factors):
        assert is_multiply_prime(a) is True

    @pytest.mark.parametrize("a, factors", [
        (30, "2*3*5"),
        (42, "2*3*7"),
        (66, "2*3*11"),
        (70, "2*5*7"),
        (78, "2*3*13"),
        (102, "2*3*17"),  # just above 100, still valid mathematically
    ])
    def test_product_of_three_distinct_primes(self, a, factors):
        assert is_multiply_prime(a) is True


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input range
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Edge-of-range inputs."""

    def test_smallest_valid_input_one(self):
        """1 is not a product of 3 primes."""
        assert is_multiply_prime(1) is False

    def test_smallest_prime(self):
        """2 is a single prime, not a product of 3."""
        assert is_multiply_prime(2) is False

    def test_largest_under_100_true(self):
        """98 = 2 * 7 * 7, exactly 3 prime factors."""
        assert is_multiply_prime(98) is True

    def test_largest_under_100_false_prime(self):
        """97 is prime itself, only 1 factor."""
        assert is_multiply_prime(97) is False

    def test_largest_under_100_false_four_factors(self):
        """96 = 2^5 * 3, six prime factors."""
        assert is_multiply_prime(96) is False

    def test_zero(self):
        """0 is not > 1, returns False."""
        assert is_multiply_prime(0) is False

    def test_negative(self):
        """Negative numbers are <= 1, return False."""
        assert is_multiply_prime(-5) is False


# ---------------------------------------------------------------------------
# Numbers that are NOT the product of exactly 3 primes
# ---------------------------------------------------------------------------

class TestNotProductOfThreePrimes:
    """Inputs that are NOT the product of exactly 3 primes → False."""

    @pytest.mark.parametrize("a, reason", [
        (1, "not > 1"),
        (2, "single prime"),
        (3, "single prime"),
        (4, "2*2, two factors"),
        (5, "single prime"),
        (6, "2*3, two factors"),
        (7, "single prime"),
        (9, "3*3, two factors"),
        (10, "2*5, two factors"),
        (14, "2*7, two factors"),
        (15, "3*5, two factors"),
        (16, "2^4, four factors"),
        (24, "2^3*3, four factors"),
        (27, "3^3, three factors — wait, this IS 3"),
        (36, "2^2*3^2, four factors"),
        (64, "2^6, six factors"),
        (100, "2^2*5^2, four factors"),
        (210, "2*3*5*7, four factors"),
    ])
    def test_not_product_of_three_primes(self, a, reason):
        result = is_multiply_prime(a)
        if a == 27:
            # 27 = 3*3*3, exactly 3 prime factors → True
            assert result is True
        else:
            assert result is False


# ---------------------------------------------------------------------------
# Edge cases around small numbers
# ---------------------------------------------------------------------------

class TestSmallNumbers:
    """Carefully check every integer from 1 to 20."""

    @pytest.mark.parametrize("a, expected", [
        (1, False),
        (2, False),   # prime
        (3, False),   # prime
        (4, False),   # 2*2
        (5, False),   # prime
        (6, False),   # 2*3
        (7, False),   # prime
        (8, True),    # 2*2*2
        (9, False),   # 3*3
        (10, False),  # 2*5
        (11, False),  # prime
        (12, True),   # 2*2*3
        (13, False),  # prime
        (14, False),  # 2*7
        (15, False),  # 3*5
        (16, False),  # 2^4
        (17, False),  # prime
        (18, True),   # 2*3*3
        (19, False),  # prime
        (20, True),   # 2*2*5
    ])
    def test_integers_1_to_20(self, a, expected):
        assert is_multiply_prime(a) is expected


# ---------------------------------------------------------------------------
# Larger numbers with known factorizations
# ---------------------------------------------------------------------------

class TestLargerNumbers:
    """Numbers between 21 and 99 with verified results."""

    @pytest.mark.parametrize("a, expected", [
        (21, False),   # 3*7
        (22, False),   # 2*11
        (23, False),   # prime
        (24, False),   # 2^3*3
        (25, False),   # 5*5
        (26, False),   # 2*13
        (27, True),    # 3*3*3
        (29, False),   # prime
        (31, False),   # prime
        (32, False),   # 2^5
        (33, False),   # 3*11
        (34, False),   # 2*17
        (35, False),   # 5*7
        (37, False),   # prime
        (38, False),   # 2*19
        (39, False),   # 3*13
        (40, False),   # 2^3*5
        (41, False),   # prime
        (43, False),   # prime
        (46, False),   # 2*23
        (47, False),   # prime
        (49, False),   # 7*7
        (51, False),   # 3*17
        (53, False),   # prime
        (55, False),   # 5*11
        (57, False),   # 3*19
        (58, False),   # 2*29
        (59, False),   # prime
        (61, False),   # prime
        (62, False),   # 2*31
        (65, False),   # 5*13
        (67, False),   # prime
        (69, False),   # 3*23
        (71, False),   # prime
        (73, False),   # prime
        (74, False),   # 2*37
        (77, False),   # 7*11
        (79, False),   # prime
        (81, False),   # 3^4
        (82, False),   # 2*41
        (83, False),   # prime
        (85, False),   # 5*17
        (86, False),   # 2*43
        (87, False),   # 3*29
        (89, False),   # prime
        (91, False),   # 7*13
        (93, False),   # 3*31
        (94, False),   # 2*47
        (95, False),   # 5*19
        (100, False),  # 2^2*5^2
    ])
    def test_remaining_numbers(self, a, expected):
        assert is_multiply_prime(a) is expected


# ---------------------------------------------------------------------------
# Type / edge-case inputs (non-standard types)
# ---------------------------------------------------------------------------

class TestEdgeCaseInputs:
    """Non-typical inputs that may or may not work."""

    @pytest.mark.parametrize("a", [
        None,
        "",
        [],
        {},
        3.5,
        -1,
        -100,
    ])
    def test_non_integer_inputs(self, a):
        """These inputs are outside the documented domain (integers < 100).
        The function may raise TypeError or return unexpected results.
        We simply verify it does not crash with an unhandled exception
        (it may return False or raise ValueError depending on implementation).
        """
        try:
            result = is_multiply_prime(a)
            # Accept any boolean result without crashing
            assert isinstance(result, bool)
        except (TypeError, ValueError):
            pass  # acceptable for out-of-domain inputs
