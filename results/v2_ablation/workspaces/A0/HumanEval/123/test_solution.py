import pytest
from solution import get_odd_collatz


class TestGetOddCollatz:
    """Tests for the get_odd_collatz function."""

    def test_n_equals_1(self):
        """Collatz(1) should return [1]."""
        assert get_odd_collatz(1) == [1]

    def test_n_equals_2(self):
        """Sequence for 2 is [2, 1], odd numbers: [1]."""
        assert get_odd_collatz(2) == [1]

    def test_n_equals_3(self):
        """Sequence for 3 is [3, 10, 5, 16, 8, 4, 2, 1], odd numbers: [1, 3, 5]."""
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_equals_5(self):
        """Sequence for 5 is [5, 16, 8, 4, 2, 1], odd numbers: [1, 5]."""
        assert get_odd_collatz(5) == [1, 5]

    def test_n_equals_7(self):
        """Sequence for 7 is [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1].
        Odd numbers: [1, 5, 7, 11, 13, 17]."""
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_equals_10(self):
        """Sequence for 10 is [10, 5, 16, 8, 4, 2, 1], odd numbers: [1, 5]."""
        assert get_odd_collatz(10) == [1, 5]

    def test_n_equals_15(self):
        """Test with a larger number that produces more odd values."""
        result = get_odd_collatz(15)
        # Verify result is sorted
        assert result == sorted(result)
        # Verify all elements are odd
        assert all(x % 2 == 1 for x in result)
        # Verify 1 is always present
        assert 1 in result

    def test_result_is_sorted(self):
        """The returned list must be sorted in increasing order."""
        for n in range(1, 100):
            result = get_odd_collatz(n)
            assert result == sorted(result), f"Result not sorted for n={n}"

    def test_all_elements_are_odd(self):
        """Every element in the returned list must be an odd number."""
        for n in range(1, 100):
            result = get_odd_collatz(n)
            assert all(x % 2 == 1 for x in result), f"Not all odd for n={n}"

    def test_always_contains_1(self):
        """The Collatz sequence always reaches 1, so 1 must be in the result."""
        for n in range(1, 100):
            result = get_odd_collatz(n)
            assert 1 in result, f"Missing 1 for n={n}"

    def test_input_is_positive_integer(self):
        """Function should work correctly for positive integers."""
        # Test a variety of positive integers
        for n in [1, 2, 3, 4, 5, 10, 100, 1000]:
            result = get_odd_collatz(n)
            assert isinstance(result, list)
            assert len(result) >= 1
            assert all(isinstance(x, int) for x in result)

    def test_even_number_with_no_odds_except_1(self):
        """For powers of 2, only 1 should appear as odd."""
        for k in range(1, 10):
            n = 2 ** k
            assert get_odd_collatz(n) == [1], f"Powers of 2 should only yield [1]"

    def test_single_element_list_for_prime_power_of_2_plus_1(self):
        """Test case where the number itself is odd and leads to a chain."""
        result = get_odd_collatz(13)
        assert 13 in result
        assert 1 in result
        assert result == sorted(result)

    def test_larger_input(self):
        """Test with a larger input to ensure correctness and no infinite loops."""
        result = get_odd_collatz(27)
        assert isinstance(result, list)
        assert len(result) > 0
        assert result == sorted(result)
        assert all(x % 2 == 1 for x in result)
        assert 1 in result

    def test_return_type_is_list(self):
        """Ensure the return type is always a list."""
        for n in range(1, 50):
            assert isinstance(get_odd_collatz(n), list)

    def test_no_duplicates_in_result(self):
        """The result list should not contain duplicate values."""
        for n in range(1, 100):
            result = get_odd_collatz(n)
            assert len(result) == len(set(result)), f"Duplicate found for n={n}"
