"""Unit tests for get_odd_collatz."""

import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:
    """Tests for the get_odd_collatz function."""

    # ------------------------------------------------------------------
    # Boundary cases at the edges of valid input ranges
    # ------------------------------------------------------------------

    def test_n_is_one(self):
        """Collatz(1) is defined as [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_is_two(self):
        """Sequence: 2 -> 1. Only odd number is 1."""
        assert get_odd_collatz(2) == [1]

    # ------------------------------------------------------------------
    # Normal cases with typical inputs
    # ------------------------------------------------------------------

    def test_n_is_three(self):
        """Sequence: 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 3, 5, 1. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_is_five(self):
        """Sequence: 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 5, 1. Sorted: [1, 5]. (Given example.)"""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_is_seven(self):
        """Sequence: 7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 7, 11, 17, 13, 5, 1. Sorted: [1, 5, 7, 11, 13, 17]."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_is_four(self):
        """Sequence: 4 -> 2 -> 1. Only odd number is 1."""
        assert get_odd_collatz(4) == [1]

    def test_n_is_six(self):
        """Sequence: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 3, 5, 1. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_is_ten(self):
        """Sequence: 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 5, 1. Sorted: [1, 5]."""
        assert get_odd_collatz(10) == [1, 5]

    def test_n_is_twelve(self):
        """Sequence: 12 -> 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 3, 5, 1. Sorted: [1, 3, 5]."""
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_n_is_twenty(self):
        """Sequence: 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 5, 1. Sorted: [1, 5]."""
        assert get_odd_collatz(20) == [1, 5]

    def test_n_is_eleven(self):
        """Sequence: 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 11, 17, 13, 5, 1. Sorted: [1, 5, 11, 13, 17]."""
        assert get_odd_collatz(11) == [1, 5, 11, 13, 17]

    def test_n_is_fifteen(self):
        """Sequence: 15 -> 46 -> 23 -> 70 -> 35 -> 106 -> 53 -> 160 -> 80 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
        Odd numbers: 15, 23, 35, 53, 5, 1. Sorted: [1, 5, 15, 23, 35, 53]."""
        assert get_odd_collatz(15) == [1, 5, 15, 23, 35, 53]

    def test_n_is_thirty(self):
        """Sequence: 30 -> 15 -> ... -> 1.
        Shares the tail of the 15 sequence after reaching 15.
        Odd numbers: 15, 23, 35, 53, 5, 1. Sorted: [1, 5, 15, 23, 35, 53]."""
        assert get_odd_collatz(30) == [1, 5, 15, 23, 35, 53]

    # ------------------------------------------------------------------
    # Additional normal cases with larger inputs
    # ------------------------------------------------------------------

    def test_n_is_27(self):
        """n=27 produces a long Collatz sequence (111 steps).
        Verifies correctness on a well-known challenging case.
        Expected odd numbers collected from the full sequence, sorted."""
        result = get_odd_collatz(27)
        # Verify the result is a list of integers, sorted, and contains 1
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)
        assert 1 in result
        assert 27 in result

    def test_n_is_100(self):
        """n=100. Sequence eventually reaches 1.
        Verify output is sorted list of odd integers containing 1."""
        result = get_odd_collatz(100)
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)
        assert 1 in result

    # ------------------------------------------------------------------
    # Property-based checks (structural guarantees)
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_result_always_contains_one(self, n):
        """Every Collatz sequence ends at 1, so 1 must always be present."""
        assert 1 in get_odd_collatz(n)

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_result_is_sorted(self, n):
        """Returned list must be sorted in increasing order."""
        result = get_odd_collatz(n)
        assert result == sorted(result)

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_all_elements_are_odd(self, n):
        """Every element in the returned list must be odd."""
        result = get_odd_collatz(n)
        assert all(x % 2 == 1 for x in result)

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_n_included_when_odd(self, n):
        """If n itself is odd, it must appear in the result."""
        if n % 2 == 1:
            assert n in get_odd_collatz(n)

    @pytest.mark.parametrize("n", [2, 4, 6, 8, 10])
    def test_n_not_included_when_even(self, n):
        """If n itself is even, it must NOT appear in the result."""
        assert n not in get_odd_collatz(n)
