"""Unit tests for count_up_to in solution.py."""

import pytest
from solution import count_up_to


# ---------------------------------------------------------------------------
# 1. Normal / typical cases (from docstring examples)
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical positive inputs documented in the docstring."""

    def test_n_equals_5(self):
        assert count_up_to(5) == [2, 3]

    def test_n_equals_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_n_equals_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_n_equals_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]


# ---------------------------------------------------------------------------
# 2. Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries where the result changes."""

    def test_n_equals_2(self):
        # 2 is the smallest prime; nothing < 2 is prime
        assert count_up_to(2) == []

    def test_n_equals_3(self):
        # Only prime strictly less than 3 is 2
        assert count_up_to(3) == [2]

    def test_n_equals_4(self):
        # Primes strictly less than 4 are 2 and 3
        assert count_up_to(4) == [2, 3]

    def test_n_equals_6(self):
        # Primes strictly less than 6 are 2, 3, 5
        assert count_up_to(6) == [2, 3, 5]

    def test_n_equals_10(self):
        # Primes strictly less than 10 are 2, 3, 5, 7
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_n_equals_100(self):
        # All primes < 100
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]
        assert count_up_to(100) == expected


# ---------------------------------------------------------------------------
# 3. Empty / zero-size inputs
# ---------------------------------------------------------------------------

class TestEmptyZeroInputs:
    """Tests where the result must be an empty list."""

    def test_n_equals_0(self):
        assert count_up_to(0) == []

    def test_n_equals_1(self):
        assert count_up_to(1) == []


# ---------------------------------------------------------------------------
# 4. Invalid inputs (negative numbers — not validated by the function)
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests with inputs outside the documented constraint (non-negative).

    Note: The current implementation does NOT raise on negative inputs;
    it silently returns [] because [True] * (n+1) with n < 0 yields [].
    These tests verify that actual (undocumented) behavior.
    """

    @pytest.mark.parametrize("n", [-1, -5, -10])
    def test_negative_returns_empty_list(self, n):
        """Negative integers produce an empty list (no validation in impl)."""
        assert count_up_to(n) == []


# ---------------------------------------------------------------------------
# 5. Additional correctness checks for larger values
# ---------------------------------------------------------------------------

class TestLargerValues:
    """Verify correctness on inputs beyond the docstring examples."""

    def test_n_equals_50(self):
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47,
        ]
        assert count_up_to(50) == expected

    def test_n_equals_30(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert count_up_to(30) == expected

    def test_result_is_sorted(self):
        """Primes should always be returned in ascending order."""
        result = count_up_to(100)
        assert result == sorted(result)

    def test_all_results_are_prime(self):
        """Every element in the result must be a prime number."""
        for n in [5, 11, 20, 50, 100]:
            for p in count_up_to(n):
                assert self._is_prime(p), f"{p} is not prime"

    @staticmethod
    def _is_prime(num):
        """Helper to verify primality independently."""
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num ** 0.5) + 1, 2):
            if num % i == 0:
                return False
        return True
