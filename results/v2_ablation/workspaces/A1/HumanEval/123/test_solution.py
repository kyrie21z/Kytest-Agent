"""Unit tests for solution.get_odd_collatz."""

import os
import sys
import pytest
from solution import get_odd_collatz


# ---------------------------------------------------------------------------
# Normal / typical cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical positive-integer inputs."""

    def test_n_5(self):
        """Example from docstring: collatz(5) -> [5, 16, 8, 4, 2, 1], odds are 1, 5."""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_1(self):
        """Collatz(1) is [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_2(self):
        """Sequence: 2 -> 1. Only odd: 1."""
        assert get_odd_collatz(2) == [1]

    def test_n_3(self):
        """Sequence: 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1. Odds: 3, 5, 1."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_4(self):
        """Sequence: 4 -> 2 -> 1. Only odd: 1."""
        assert get_odd_collatz(4) == [1]

    def test_n_6(self):
        """Sequence: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1. Odds: 3, 5, 1."""
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_7(self):
        """Sequence: 7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
           Odds: 7, 11, 17, 13, 5, 1."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_9(self):
        """Sequence: 9 -> 28 -> 14 -> 7 -> ... -> 1.
           Odds encountered: 9, 7, 11, 17, 13, 5, 1."""
        assert get_odd_collatz(9) == [1, 5, 7, 9, 11, 13, 17]

    def test_n_10(self):
        """Sequence: 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1. Odds: 5, 1."""
        assert get_odd_collatz(10) == [1, 5]

    def test_n_11(self):
        """Sequence: 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
           Odds: 11, 17, 13, 5, 1."""
        assert get_odd_collatz(11) == [1, 5, 11, 13, 17]

    def test_n_12(self):
        """Sequence: 12 -> 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1. Odds: 3, 5, 1."""
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_n_15(self):
        """Sequence: 15 -> 46 -> 23 -> 70 -> 35 -> 106 -> 53 -> 160 -> 80 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
           Odds: 15, 23, 35, 53, 5, 1."""
        assert get_odd_collatz(15) == [1, 5, 15, 23, 35, 53]

    def test_n_18(self):
        """Sequence: 18 -> 9 -> ... -> 1. Shares tail with n=9.
           Odds: 9, 7, 11, 17, 13, 5, 1."""
        assert get_odd_collatz(18) == [1, 5, 7, 9, 11, 13, 17]

    def test_n_20(self):
        """Sequence: 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1. Odds: 5, 1."""
        assert get_odd_collatz(20) == [1, 5]

    def test_n_21(self):
        """Sequence: 21 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1.
           Wait: 21 is odd -> 3*21+1 = 64. Then 64->32->16->8->4->2->1.
           Odds: 21, 1."""
        assert get_odd_collatz(21) == [1, 21]

    def test_n_22(self):
        """Sequence: 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
           Odds: 11, 17, 13, 5, 1."""
        assert get_odd_collatz(22) == [1, 5, 11, 13, 17]

    def test_n_27(self):
        """A well-known case with a long sequence.
           We verify programmatically below."""
        result = get_odd_collatz(27)
        # Verify: every element is odd, result is sorted, and 1 is present
        assert 1 in result
        assert all(x % 2 == 1 for x in result)
        assert result == sorted(result)
        # Known: 27 reaches 1 after 111 steps; there are many odd numbers
        assert len(result) > 10

    def test_n_100(self):
        """Larger even number. Verify correctness structurally."""
        result = get_odd_collatz(100)
        assert 1 in result
        assert all(x % 2 == 1 for x in result)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_input_n_1(self):
        """Minimum valid input."""
        assert get_odd_collatz(1) == [1]

    def test_largest_single_digit_n_9(self):
        """Maximum single-digit input."""
        assert get_odd_collatz(9) == [1, 5, 7, 9, 11, 13, 17]

    def test_two_digit_boundary_n_99(self):
        """Just before three digits."""
        result = get_odd_collatz(99)
        assert 1 in result
        assert all(x % 2 == 1 for x in result)
        assert result == sorted(result)

    def test_power_of_two_n_16(self):
        """Power of two: only odd number is 1."""
        assert get_odd_collatz(16) == [1]

    def test_power_of_two_n_32(self):
        assert get_odd_collatz(32) == [1]

    def test_power_of_two_n_64(self):
        assert get_odd_collatz(64) == [1]

    def test_even_number_with_no_other_odds_n_2(self):
        """Smallest even number whose sequence contains no odd besides 1."""
        assert get_odd_collatz(2) == [1]


# ---------------------------------------------------------------------------
# Empty / zero-size / null-like inputs
# ---------------------------------------------------------------------------

class TestEdgeInputs:
    """Tests for inputs that are zero, negative, or otherwise non-positive."""

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="signal.alarm is not available on Windows"
    )
    def test_n_zero(self):
        """n=0 is not a positive integer. The function enters an infinite loop
        because 0 is even and 0//2 == 0 forever. We expect a timeout."""
        with pytest.raises(TimeoutError):
            import signal
            signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimeoutError()))
            signal.alarm(1)
            try:
                get_odd_collatz(0)
            finally:
                signal.alarm(0)

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="signal.alarm is not available on Windows"
    )
    def test_n_negative(self):
        """Negative inputs are not documented as valid. They may loop or diverge."""
        with pytest.raises(TimeoutError):
            import signal
            signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimeoutError()))
            signal.alarm(1)
            try:
                get_odd_collatz(-5)
            finally:
                signal.alarm(0)


# ---------------------------------------------------------------------------
# Invalid inputs (wrong types)
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests for inputs of incorrect types."""

    def test_none_input(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            get_odd_collatz(None)

    def test_string_input(self):
        """Passing a string should raise TypeError."""
        with pytest.raises(TypeError):
            get_odd_collatz("5")

    def test_list_input(self):
        """Passing a list should raise TypeError."""
        with pytest.raises(TypeError):
            get_odd_collatz([5])

    def test_dict_input(self):
        """Passing a dict should raise TypeError."""
        with pytest.raises(TypeError):
            get_odd_collatz({"n": 5})

    def test_tuple_input(self):
        """Passing a tuple should raise TypeError."""
        with pytest.raises(TypeError):
            get_odd_collatz((5,))


# ---------------------------------------------------------------------------
# Structural / property-based checks
# ---------------------------------------------------------------------------

class TestStructuralProperties:
    """General properties that should hold for any valid positive integer n."""

    @pytest.mark.parametrize("n", range(1, 200))
    def test_all_elements_odd(self, n):
        """Every element in the returned list must be odd."""
        result = get_odd_collatz(n)
        assert all(x % 2 == 1 for x in result), f"Non-odd element found for n={n}"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_result_sorted(self, n):
        """Returned list must be sorted in increasing order."""
        result = get_odd_collatz(n)
        assert result == sorted(result), f"Not sorted for n={n}"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_contains_one(self, n):
        """The Collatz sequence always reaches 1, so 1 must be in the result."""
        result = get_odd_collatz(n)
        assert 1 in result, f"Missing 1 for n={n}"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_n_included_if_odd(self, n):
        """If n itself is odd, it must appear in the result."""
        result = get_odd_collatz(n)
        if n % 2 == 1:
            assert n in result, f"n={n} is odd but missing from result"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_n_not_included_if_even(self, n):
        """For even n, n itself is even so it should NOT be in the result."""
        result = get_odd_collatz(n)
        if n % 2 == 0:
            assert n not in result, f"n={n} is even but appears in result"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_non_empty_result(self, n):
        """Result must never be empty (at minimum contains 1)."""
        result = get_odd_collatz(n)
        assert len(result) >= 1, f"Empty result for n={n}"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_result_type_is_list(self, n):
        """Return type must be a list."""
        result = get_odd_collatz(n)
        assert isinstance(result, list), f"Expected list, got {type(result)}"

    @pytest.mark.parametrize("n", range(1, 200))
    def test_result_elements_are_integers(self, n):
        """All elements must be integers."""
        result = get_odd_collatz(n)
        assert all(isinstance(x, int) for x in result), f"Non-int element for n={n}"
