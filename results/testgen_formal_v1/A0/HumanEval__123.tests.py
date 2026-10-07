import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:
    """Unit tests for the get_odd_collatz function."""

    # --- Basic / documented examples ---

    def test_n_equals_1(self):
        """Collatz(1) should return [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_equals_5(self):
        """Example from docstring: Collatz(5) -> [1, 5]."""
        assert get_odd_collatz(5) == [1, 5]

    # --- Small positive integers ---

    def test_n_equals_2(self):
        """Sequence: 2 -> 1; only odd number is 1."""
        assert get_odd_collatz(2) == [1]

    def test_n_equals_3(self):
        """Sequence: 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1; odds: 3, 5, 1."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_equals_4(self):
        """Sequence: 4 -> 2 -> 1; only odd number is 1."""
        assert get_odd_collatz(4) == [1]

    def test_n_equals_6(self):
        """Sequence: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1; odds: 3, 5, 1."""
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_equals_7(self):
        """Sequence: 7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1"""
        result = get_odd_collatz(7)
        assert result == [1, 5, 7, 11, 13, 17]

    def test_n_equals_8(self):
        """Sequence: 8 -> 4 -> 2 -> 1; only odd number is 1."""
        assert get_odd_collatz(8) == [1]

    def test_n_equals_9(self):
        """Sequence: 9 -> 28 -> 14 -> 7 -> ... -> 1; odds include 9, 7, 5, 11, 13, 17, 1."""
        assert get_odd_collatz(9) == [1, 5, 7, 9, 11, 13, 17]

    def test_n_equals_10(self):
        """Sequence: 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1; odds: 5, 1."""
        assert get_odd_collatz(10) == [1, 5]

    # --- Larger values ---

    def test_n_equals_15(self):
        """A moderately large value with several odd terms."""
        assert get_odd_collatz(15) == [1, 5, 15, 23, 35, 53]

    def test_n_equals_27(self):
        """27 has a long Collatz sequence with many odd numbers."""
        result = get_odd_collatz(27)
        # Verify the result is sorted and contains expected elements
        assert result == sorted(result)
        assert 1 in result
        assert 27 in result

    def test_n_equals_100(self):
        """Even number whose Collatz path eventually hits odd numbers."""
        result = get_odd_collatz(100)
        assert result == sorted(result)
        assert 1 in result

    # --- Return type checks ---

    def test_returns_list(self):
        """The return value must be a list."""
        assert isinstance(get_odd_collatz(1), list)

    def test_returns_sorted(self):
        """Returned list must always be in increasing order."""
        for n in range(1, 101):
            result = get_odd_collatz(n)
            assert result == sorted(result), f"Not sorted for n={n}"

    def test_contains_only_odd_numbers(self):
        """Every element in the returned list must be odd."""
        for n in range(1, 101):
            result = get_odd_collatz(n)
            for val in result:
                assert val % 2 == 1, f"Even number {val} found for n={n}"

    def test_always_contains_1(self):
        """The Collatz sequence always reaches 1, so 1 must be in every result."""
        for n in range(1, 101):
            assert 1 in get_odd_collatz(n), f"Missing 1 for n={n}"

    def test_contains_n_when_n_is_odd(self):
        """If n is odd, n itself must appear in the result."""
        for n in range(1, 101, 2):
            assert n in get_odd_collatz(n), f"Missing {n} for odd n={n}"

    # --- Edge cases ---

    def test_single_element_for_power_of_two(self):
        """Powers of two have only one odd number (1) in their Collatz sequence."""
        for exp in range(1, 10):
            n = 2 ** exp
            assert get_odd_collatz(n) == [1], f"Expected [1] for n={n}"

    def test_large_input(self):
        """Test with a larger input to ensure correctness and no overflow issues."""
        result = get_odd_collatz(9999)
        assert result == sorted(result)
        assert 1 in result
        assert 9999 in result

    # --- Invalid / unexpected inputs ---

    def test_zero_raises_or_returns_empty(self):
        """n=0 is not a positive integer; the function may raise or behave gracefully."""
        with pytest.raises(Exception):
            get_odd_collatz(0)

    def test_negative_number_raises_or_behaves_gracefully(self):
        """Negative numbers are not valid inputs."""
        with pytest.raises(Exception):
            get_odd_collatz(-5)

    def test_non_integer_raises(self):
        """Non-integer inputs should raise an error."""
        with pytest.raises(Exception):
            get_odd_collatz(3.5)

    def test_string_input_raises(self):
        """String inputs should raise an error."""
        with pytest.raises(Exception):
            get_odd_collatz("hello")
