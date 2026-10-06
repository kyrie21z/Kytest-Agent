"""Unit tests for solution.get_odd_collatz."""
import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:
    """Tests covering normal, boundary, empty/edge, and invalid inputs."""

    # ── Normal cases ────────────────────────────────────────────────

    def test_n_1(self):
        """Collatz(1) is [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_2(self):
        """Sequence: 2 → 1; odd numbers: [1]."""
        assert get_odd_collatz(2) == [1]

    def test_n_3(self):
        """Sequence: 3, 10, 5, 16, 8, 4, 2, 1; odds: [1, 3, 5]."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_5(self):
        """Sequence: 5, 16, 8, 4, 2, 1; odds: [1, 5]."""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_7(self):
        """Sequence: 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_10(self):
        """Sequence: 10, 5, 16, 8, 4, 2, 1; odds: [1, 5]."""
        assert get_odd_collatz(10) == [1, 5]

    def test_n_12(self):
        """Sequence: 12, 6, 3, 10, 5, 16, 8, 4, 2, 1; odds: [1, 3, 5]."""
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_n_20(self):
        """Sequence: 20, 10, 5, 16, 8, 4, 2, 1; odds: [1, 5]."""
        assert get_odd_collatz(20) == [1, 5]

    def test_n_27(self):
        """Larger number with many odd terms."""
        result = get_odd_collatz(27)
        # Verify sorted order
        assert result == sorted(result)
        # Must contain 1 and 27
        assert 1 in result
        assert 27 in result

    # ── Boundary cases ──────────────────────────────────────────────

    def test_n_large_prime(self):
        """n = 97 (a prime); should still terminate and return sorted list."""
        result = get_odd_collatz(97)
        assert result == sorted(result)
        assert 1 in result
        assert 97 in result

    def test_n_power_of_two(self):
        """Powers of two only have 1 as the odd number."""
        for p in [1, 2, 4, 8, 16, 32, 64]:
            assert get_odd_collatz(p) == [1], f"Failed for n={p}"

    def test_n_even_with_odds(self):
        """n = 6 → 6, 3, 10, 5, 16, 8, 4, 2, 1; odds: [1, 3, 5]."""
        assert get_odd_collatz(6) == [1, 3, 5]

    # ── Invalid / edge-case inputs ──────────────────────────────────

    def test_n_zero_raises_or_returns_empty(self):
        """n=0 is not a positive integer; function should raise ValueError."""
        with pytest.raises(ValueError):
            get_odd_collatz(0)

    def test_n_negative_raises(self):
        """Negative input should raise ValueError."""
        with pytest.raises(ValueError):
            get_odd_collatz(-5)

    def test_n_float_raises(self):
        """Non-integer input should raise TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            get_odd_collatz(3.5)

    def test_n_string_raises(self):
        """String input should raise TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            get_odd_collatz("5")

    # ── Output property checks ──────────────────────────────────────

    def test_output_is_list(self):
        """Return type must be a list."""
        assert isinstance(get_odd_collatz(5), list)

    def test_output_sorted_increasing(self):
        """Output must always be sorted in increasing order."""
        for n in range(1, 101):
            result = get_odd_collatz(n)
            assert result == sorted(result), f"Not sorted for n={n}"

    def test_no_duplicates(self):
        """Each odd number should appear at most once."""
        for n in range(1, 101):
            result = get_odd_collatz(n)
            assert len(result) == len(set(result)), f"Duplicates found for n={n}"

    def test_all_elements_are_integers(self):
        """Every element must be an int."""
        for n in range(1, 101):
            result = get_odd_collatz(n)
            assert all(isinstance(x, int) for x in result), f"Non-int in result for n={n}"

    def test_result_contains_one(self):
        """Result must always contain 1 (the conjecture guarantees reaching 1)."""
        for n in range(1, 101):
            assert 1 in get_odd_collatz(n), f"Missing 1 for n={n}"

    def test_result_contains_input_when_odd(self):
        """If n is odd, it must appear in the result."""
        for n in range(1, 101, 2):
            assert n in get_odd_collatz(n), f"Missing {n} for odd n={n}"
