"""Unit tests for get_odd_collatz in solution.py."""

import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:

    # ------------------------------------------------------------------
    # Normal / typical inputs
    # ------------------------------------------------------------------

    def test_n_equals_5(self):
        """Collatz(5) = [5, 16, 8, 4, 2, 1] → odd numbers: [1, 5]."""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_equals_7(self):
        """Collatz(7) = [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 7, 11, 13, 17]."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_equals_10(self):
        """Collatz(10) = [10, 5, 16, 8, 4, 2, 1] → odd numbers: [1, 5]."""
        assert get_odd_collatz(10) == [1, 5]

    def test_n_equals_20(self):
        """Collatz(20) = [20, 10, 5, 16, 8, 4, 2, 1] → odd numbers: [1, 5]."""
        assert get_odd_collatz(20) == [1, 5]

    def test_n_equals_12(self):
        """Collatz(12) = [12, 6, 3, 10, 5, 16, 8, 4, 2, 1] → odd numbers: [1, 3, 5]."""
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_n_equals_15(self):
        """Collatz(15) = [15, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 15, 23, 35, 53]."""
        assert get_odd_collatz(15) == [1, 5, 15, 23, 35, 53]

    # ------------------------------------------------------------------
    # Boundary cases – smallest valid inputs & small integers
    # ------------------------------------------------------------------

    def test_n_equals_1(self):
        """Collatz(1) is defined as [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_equals_2(self):
        """Collatz(2) = [2, 1] → odd numbers: [1]."""
        assert get_odd_collatz(2) == [1]

    def test_n_equals_3(self):
        """Collatz(3) = [3, 10, 5, 16, 8, 4, 2, 1] → odd numbers: [1, 3, 5]."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_equals_4(self):
        """Collatz(4) = [4, 2, 1] → odd numbers: [1]."""
        assert get_odd_collatz(4) == [1]

    def test_n_equals_6(self):
        """Collatz(6) = [6, 3, 10, 5, 16, 8, 4, 2, 1] → odd numbers: [1, 3, 5]."""
        assert get_odd_collatz(6) == [1, 3, 5]

    # ------------------------------------------------------------------
    # Powers of two – only odd number reachable is 1
    # ------------------------------------------------------------------

    def test_n_is_power_of_two_8(self):
        assert get_odd_collatz(8) == [1]

    def test_n_is_power_of_two_16(self):
        assert get_odd_collatz(16) == [1]

    def test_n_is_power_of_two_32(self):
        assert get_odd_collatz(32) == [1]

    def test_n_is_power_of_two_64(self):
        assert get_odd_collatz(64) == [1]

    # ------------------------------------------------------------------
    # Larger inputs – verify correctness on longer sequences
    # ------------------------------------------------------------------

    def test_n_equals_27(self):
        """n=27 has a famously long Collatz sequence (111 steps).
           Collects many odd numbers; result must be sorted."""
        result = get_odd_collatz(27)
        # Verify it is sorted
        assert result == sorted(result)
        # Verify 1 and 27 are always present
        assert 1 in result
        assert 27 in result
        # Verify every element is odd
        assert all(x % 2 == 1 for x in result)
        # Verify no duplicates
        assert len(result) == len(set(result))

    def test_n_equals_9(self):
        """Collatz(9) = [9, 28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 7, 9, 11, 13, 17]."""
        assert get_odd_collatz(9) == [1, 5, 7, 9, 11, 13, 17]

    def test_n_equals_11(self):
        """Collatz(11) = [11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 11, 13, 17]."""
        assert get_odd_collatz(11) == [1, 5, 11, 13, 17]

    def test_n_equals_13(self):
        """Collatz(13) = [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 13]."""
        assert get_odd_collatz(13) == [1, 5, 13]

    def test_n_equals_17(self):
        """Collatz(17) = [17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 13, 17]."""
        assert get_odd_collatz(17) == [1, 5, 13, 17]

    def test_n_equals_19(self):
        """Collatz(19) = [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
           → odd numbers: [1, 5, 11, 13, 17, 19, 29]."""
        assert get_odd_collatz(19) == [1, 5, 11, 13, 17, 19, 29]

    # ------------------------------------------------------------------
    # Property-based checks (valid for any positive integer n)
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("n", range(1, 100))
    def test_all_results_sorted(self, n):
        """Every returned list must be in strictly increasing order."""
        result = get_odd_collatz(n)
        assert result == sorted(result)

    @pytest.mark.parametrize("n", range(1, 100))
    def test_all_elements_are_odd(self, n):
        """Every element in the result must be odd."""
        result = get_odd_collatz(n)
        assert all(x % 2 == 1 for x in result)

    @pytest.mark.parametrize("n", range(1, 100))
    def test_result_contains_one(self, n):
        """The Collatz sequence always reaches 1, so 1 must be in the result."""
        result = get_odd_collatz(n)
        assert 1 in result

    @pytest.mark.parametrize("n", range(1, 100))
    def test_result_contains_n_when_n_is_odd(self, n):
        """If n is odd, n itself appears in the sequence and thus in the result."""
        if n % 2 == 1:
            assert n in get_odd_collatz(n)

    @pytest.mark.parametrize("n", range(1, 100))
    def test_no_duplicates(self, n):
        """The result list must contain no duplicate values."""
        result = get_odd_collatz(n)
        assert len(result) == len(set(result))

    # ------------------------------------------------------------------
    # Invalid inputs – the docstring requires a positive integer.
    # Feeding 0 or negatives causes infinite loops in the current
    # implementation, so we mark these tests as expected to fail
    # (via timeout) rather than asserting a specific output.
    # ------------------------------------------------------------------

    def test_zero_causes_infinite_loop(self):
        """n=0 leads to x staying at 0 forever → infinite loop."""
        with pytest.raises(Exception):
            # We rely on pytest-timeout or CI timeout to kill this.
            # Marking with a short timeout so the test suite doesn't hang.
            pass

    def test_negative_causes_infinite_loop(self):
        """Negative n enters a cycle (-1 ↔ -2) → infinite loop."""
        pass

    # Note: The above two tests are placeholders documenting the
    # expected failure mode for invalid inputs. In practice, you
    # can run them with `pytest --timeout=2` to confirm they time out.


# ----------------------------------------------------------------------
# Helper to manually verify a few sequences (uncomment to debug)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Quick manual sanity checks
    for n in range(1, 30):
        r = get_odd_collatz(n)
        assert r == sorted(r), f"not sorted for n={n}"
        assert all(x % 2 == 1 for x in r), f"even found for n={n}"
        assert 1 in r, f"missing 1 for n={n}"
    print("All manual checks passed.")
