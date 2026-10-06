"""Unit tests for count_up_to in solution.py."""

import pytest
from solution import count_up_to


# ── Normal / typical cases ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical positive inputs matching the docstring examples."""

    def test_n_equals_5(self):
        assert count_up_to(5) == [2, 3]

    def test_n_equals_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_n_equals_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_n_equals_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]

    def test_n_equals_10(self):
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_n_equals_30(self):
        assert count_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    def test_n_equals_100(self):
        assert count_up_to(100) == [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]


# ── Boundary cases at edges of valid input ranges ───────────────────────

class TestBoundaryCases:
    """Tests at the lower boundary where few or no primes exist below n."""

    def test_n_equals_0(self):
        """No primes less than 0."""
        assert count_up_to(0) == []

    def test_n_equals_1(self):
        """No primes less than 1."""
        assert count_up_to(1) == []

    def test_n_equals_2(self):
        """2 is the smallest prime, but we want primes < 2, so none."""
        assert count_up_to(2) == []

    def test_n_equals_3(self):
        """Only prime strictly less than 3 is 2."""
        assert count_up_to(3) == [2]

    def test_n_equals_4(self):
        """Primes less than 4 are 2 and 3."""
        assert count_up_to(4) == [2, 3]

    def test_n_equals_6(self):
        """Primes less than 6: 2, 3, 5."""
        assert count_up_to(6) == [2, 3, 5]

    def test_n_equals_7(self):
        """Primes less than 7: 2, 3, 5."""
        assert count_up_to(7) == [2, 3, 5]

    def test_n_equals_8(self):
        """Primes less than 8: 2, 3, 5, 7."""
        assert count_up_to(8) == [2, 3, 5, 7]


# ── Empty, null, or zero-size inputs ────────────────────────────────────

class TestEmptyAndZeroInputs:
    """Tests for edge-case inputs that produce empty results."""

    def test_n_is_zero(self):
        assert count_up_to(0) == []

    def test_n_is_one(self):
        assert count_up_to(1) == []

    def test_n_is_two(self):
        assert count_up_to(2) == []


# ── Invalid inputs ──────────────────────────────────────────────────────

class TestInvalidInputs:
    """Tests for inputs outside the documented 'non-negative integer' constraint."""

    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_negative_integer(self, n):
        """Negative integers are not documented; verify current behaviour."""
        # With negative n, range(2, n) is empty and isprime has length <= 0,
        # so the function returns an empty list without raising.
        assert count_up_to(n) == []

    @pytest.mark.parametrize("n", [None, "abc", 3.5, True, False])
    def test_non_integer_types(self, n):
        """Non-integer types may cause unexpected behaviour; just ensure no crash."""
        try:
            result = count_up_to(n)
            # If it doesn't raise, at least return something iterable
            assert isinstance(result, list)
        except (TypeError, ValueError):
            pass  # Acceptable — the function isn't required to handle these


# ── Exception / stress cases ────────────────────────────────────────────

class TestStressCases:
    """Larger inputs to exercise correctness and performance."""

    def test_n_equals_1000(self):
        """Verify first 168 primes (< 1000)."""
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
            127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
            179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
            233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
            283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
            353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
            419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
            467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
            547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
            607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
            661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
            739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
            811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
            877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
            947, 953, 967, 971, 977, 983, 991, 997,
        ]
        assert count_up_to(1000) == expected

    def test_n_equals_50(self):
        assert count_up_to(50) == [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47,
        ]

    def test_result_is_list(self):
        """Return value should always be a list."""
        for n in [0, 1, 2, 5, 10, 100]:
            assert isinstance(count_up_to(n), list)

    def test_result_sorted(self):
        """Result should be in ascending order."""
        for n in [5, 10, 50, 100, 500, 1000]:
            result = count_up_to(n)
            assert result == sorted(result)

    def test_no_duplicates(self):
        """Each prime should appear exactly once."""
        for n in [5, 10, 50, 100, 500, 1000]:
            result = count_up_to(n)
            assert len(result) == len(set(result))

    def test_all_elements_are_prime(self):
        """Every element in the result must actually be prime."""
        def is_prime(x):
            if x < 2:
                return False
            if x < 4:
                return True
            if x % 2 == 0 or x % 3 == 0:
                return False
            i = 5
            while i * i <= x:
                if x % i == 0 or x % (i + 2) == 0:
                    return False
                i += 6
            return True

        for n in [5, 10, 50, 100, 500, 1000]:
            result = count_up_to(n)
            for p in result:
                assert is_prime(p), f"{p} is not prime"

    def test_all_primes_less_than_n_included(self):
        """Every prime < n must appear in the result."""
        def primes_less_than(limit):
            sieve = [True] * limit
            for i in range(2, int(limit ** 0.5) + 1):
                if sieve[i]:
                    for j in range(i * i, limit, i):
                        sieve[j] = False
            return [i for i in range(2, limit) if sieve[i]]

        for n in [5, 10, 50, 100, 500, 1000]:
            expected = primes_less_than(n)
            assert count_up_to(n) == expected
