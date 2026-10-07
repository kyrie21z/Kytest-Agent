"""Unit tests for count_up_to in solution.py.

The function count_up_to(n) returns a list of all prime numbers strictly
less than n. It accepts non-negative integers.

Test categories:
  1. Normal cases – typical documented inputs.
  2. Boundary cases – edges of valid input ranges.
  3. Empty / zero-size inputs.
  4. Invalid inputs – negative numbers, non-integers.
  5. Exception cases – inputs that raise errors.
"""

import pytest
from solution import count_up_to


# ──────────────────────────────────────────────
# 1. Normal cases (typical documented inputs)
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests against the examples given in the docstring."""

    def test_count_up_to_5(self):
        assert count_up_to(5) == [2, 3]

    def test_count_up_to_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_count_up_to_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_count_up_to_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]

    # Additional normal cases not in the docstring
    def test_count_up_to_10(self):
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_count_up_to_30(self):
        assert count_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    def test_count_up_to_100(self):
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]
        assert count_up_to(100) == expected


# ──────────────────────────────────────────────
# 2. Boundary cases (edges of valid range)
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the lower boundary where few or no primes exist."""

    def test_n_is_2(self):
        """No primes < 2."""
        assert count_up_to(2) == []

    def test_n_is_3(self):
        """Only one prime < 3."""
        assert count_up_to(3) == [2]

    def test_n_is_4(self):
        """Primes < 4 are 2, 3."""
        assert count_up_to(4) == [2, 3]

    def test_n_is_prime_boundary(self):
        """When n itself is prime, it should NOT be included."""
        assert count_up_to(7) == [2, 3, 5]

    def test_n_is_prime_boundary_13(self):
        assert count_up_to(13) == [2, 3, 5, 7, 11]

    def test_n_is_prime_boundary_17(self):
        assert count_up_to(17) == [2, 3, 5, 7, 11, 13]


# ──────────────────────────────────────────────
# 3. Empty / zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyAndZeroInputs:
    """Tests for inputs that produce empty results."""

    def test_zero(self):
        assert count_up_to(0) == []

    def test_one(self):
        assert count_up_to(1) == []


# ──────────────────────────────────────────────
# 4. Invalid inputs (negative, non-integer)
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests for inputs outside the documented 'non-negative integer' constraint.

    Note: The current implementation does NOT validate input types. Negative
    integers silently return [] because [True] * (n+1) with n < -1 yields [].
    Non-integer types (float, str, None, list) DO raise TypeError via range().
    """

    def test_negative_input_returns_empty_list(self):
        """Negative n: the sieve array becomes empty, range is empty → [].
        The function does NOT raise; it just returns [].
        """
        assert count_up_to(-1) == []

    def test_large_negative_returns_empty_list(self):
        assert count_up_to(-100) == []

    def test_float_input_raises(self):
        """A float passed to range() as stop raises TypeError."""
        with pytest.raises(TypeError):
            count_up_to(5.0)

    def test_string_input_raises(self):
        with pytest.raises(TypeError):
            count_up_to("5")

    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            count_up_to(None)

    def test_list_input_raises(self):
        with pytest.raises(TypeError):
            count_up_to([5])


# ──────────────────────────────────────────────
# 5. Exception & edge-case verification
# ──────────────────────────────────────────────

class TestExceptionsAndEdgeCases:
    """Additional exception and correctness checks."""

    def test_returns_list_type(self):
        result = count_up_to(10)
        assert isinstance(result, list)

    def test_no_duplicates(self):
        """Each prime should appear exactly once."""
        result = count_up_to(100)
        assert len(result) == len(set(result))

    def test_all_elements_are_integers(self):
        result = count_up_to(50)
        assert all(isinstance(x, int) for x in result)

    def test_result_sorted(self):
        result = count_up_to(200)
        assert result == sorted(result)

    def test_no_composites_in_result(self):
        """Verify none of the returned values are composite."""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        result = count_up_to(500)
        assert all(is_prime(x) for x in result)

    def test_all_primes_less_than_n_included(self):
        """Cross-check: every prime < n must be present."""
        def primes_upto(limit):
            sieve = [True] * limit
            for p in range(2, int(limit ** 0.5) + 1):
                if sieve[p]:
                    for multiple in range(p * p, limit, p):
                        sieve[multiple] = False
            return [p for p in range(2, limit) if sieve[p]]

        for n in [5, 10, 20, 50, 100, 200, 500]:
            assert count_up_to(n) == primes_upto(n)

    def test_large_input(self):
        """Ensure the function handles a reasonably large input without error."""
        result = count_up_to(10000)
        # There are 1229 primes below 10000
        assert len(result) == 1229
        assert result[-1] == 9973  # largest prime < 10000
