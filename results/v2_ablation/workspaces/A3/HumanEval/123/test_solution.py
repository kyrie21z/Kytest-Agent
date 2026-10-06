"""Unit tests for solution.get_odd_collatz."""
import pytest
from solution import get_odd_collatz


class TestGetOddCollatzNormalCases:
    """Test normal/typical inputs."""

    def test_n_5(self):
        # Collatz(5) = [5, 16, 8, 4, 2, 1] -> odds: [1, 5]
        assert get_odd_collatz(5) == [1, 5]

    def test_n_3(self):
        # Collatz(3) = [3, 10, 5, 16, 8, 4, 2, 1] -> odds: [1, 3, 5]
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_6(self):
        # Collatz(6) = [6, 3, 10, 5, 16, 8, 4, 2, 1] -> odds: [1, 3, 5]
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_7(self):
        # Collatz(7) = [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # Odds: 7, 11, 17, 13, 5, 1 -> sorted: [1, 5, 7, 11, 13, 17]
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_9(self):
        # Collatz(9) has many steps; collect all odd numbers and sort.
        # Sequence: 9, 28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1
        # Odds: 9, 7, 11, 17, 13, 5, 1 -> sorted: [1, 5, 7, 9, 11, 13, 17]
        assert get_odd_collatz(9) == [1, 5, 7, 9, 11, 13, 17]

    def test_n_10(self):
        # Collatz(10) = [10, 5, 16, 8, 4, 2, 1] -> odds: [1, 5]
        assert get_odd_collatz(10) == [1, 5]

    def test_n_11(self):
        # Collatz(11) = [11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # Odds: 11, 17, 13, 5, 1 -> sorted: [1, 5, 11, 13, 17]
        assert get_odd_collatz(11) == [1, 5, 11, 13, 17]


class TestGetOddCollatzBoundaryCases:
    """Test boundary values at edges of valid input range."""

    def test_n_1_minimal(self):
        # Collatz(1) is defined as [1] per the docstring.
        assert get_odd_collatz(1) == [1]

    def test_n_2(self):
        # Collatz(2) = [2, 1] -> odds: [1]
        assert get_odd_collatz(2) == [1]

    def test_n_4_power_of_two(self):
        # Collatz(4) = [4, 2, 1] -> odds: [1]
        assert get_odd_collatz(4) == [1]

    def test_n_8_power_of_two(self):
        # Collatz(8) = [8, 4, 2, 1] -> odds: [1]
        assert get_odd_collatz(8) == [1]

    def test_n_16_power_of_two(self):
        # Collatz(16) = [16, 8, 4, 2, 1] -> odds: [1]
        assert get_odd_collatz(16) == [1]

    def test_n_27_long_sequence(self):
        # n=27 produces a long sequence (111 steps). Just verify it returns
        # a non-empty list containing 1 and 27, and that the result is sorted.
        result = get_odd_collatz(27)
        assert isinstance(result, list)
        assert len(result) > 1
        assert result[0] == 1
        assert 27 in result
        assert result == sorted(result)


class TestGetOddCollatzReturnProperties:
    """Test properties of the return value."""

    def test_returns_list(self):
        assert isinstance(get_odd_collatz(5), list)

    def test_result_sorted_increasing(self):
        result = get_odd_collatz(27)
        assert result == sorted(result)

    def test_always_contains_1(self):
        # Every Collatz sequence reaches 1, so 1 must always be in the result.
        for n in [1, 2, 3, 5, 7, 10, 27]:
            assert 1 in get_odd_collatz(n)

    def test_all_elements_are_odd(self):
        # Every element in the returned list must be odd.
        for n in [1, 2, 3, 5, 7, 10, 27]:
            result = get_odd_collatz(n)
            for val in result:
                assert val % 2 == 1

    def test_n_equals_1_single_element(self):
        # When n=1, the only odd number is 1 itself.
        assert get_odd_collatz(1) == [1]

    def test_prime_number(self):
        # Test with a prime number like 13.
        # Collatz(13) = [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # Odds: 13, 5, 1 -> sorted: [1, 5, 13]
        assert get_odd_collatz(13) == [1, 5, 13]

    def test_even_input_with_odd_in_sequence(self):
        # n=12 -> [12, 6, 3, 10, 5, 16, 8, 4, 2, 1]
        # Odds: 3, 5, 1 -> sorted: [1, 3, 5]
        assert get_odd_collatz(12) == [1, 3, 5]
