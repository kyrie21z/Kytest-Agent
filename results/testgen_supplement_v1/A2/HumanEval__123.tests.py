import pytest
from solution import get_odd_collatz


class TestGetOddCollatzNormalCases:
    """Tests with typical positive integer inputs."""

    def test_n_equals_5(self):
        # Collatz(5) = [5, 16, 8, 4, 2, 1], odd numbers: 5, 1
        assert get_odd_collatz(5) == [1, 5]

    def test_n_equals_10(self):
        # Collatz(10) = [10, 5, 16, 8, 4, 2, 1], odd numbers: 5, 1
        assert get_odd_collatz(10) == [1, 5]

    def test_n_equals_7(self):
        # Collatz(7) = [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 7, 11, 17, 13, 5, 1
        assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]

    def test_n_equals_12(self):
        # Collatz(12) = [12, 6, 3, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 3, 5, 1
        assert get_odd_collatz(12) == [1, 3, 5]

    def test_n_equals_3(self):
        # Collatz(3) = [3, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 3, 5, 1
        assert get_odd_collatz(3) == [1, 3, 5]

    def test_n_equals_6(self):
        # Collatz(6) = [6, 3, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 3, 5, 1
        assert get_odd_collatz(6) == [1, 3, 5]

    def test_n_equals_20(self):
        # Collatz(20) = [20, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 5, 1
        assert get_odd_collatz(20) == [1, 5]

    def test_n_equals_27(self):
        # Collatz(27) has many terms; verified via execution
        assert get_odd_collatz(27) == [1, 5, 23, 27, 31, 35, 41, 47, 53, 61, 71, 91, 103, 107, 121, 137, 155, 161, 167, 175, 233, 251, 263, 283, 319, 325, 377, 395, 425, 433, 445, 479, 577, 593, 719, 911, 1079, 1367, 1619, 2051, 2429, 3077]


class TestGetOddCollatzBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_n_equals_1_minimal(self):
        # Collatz(1) = [1], only odd number is 1
        assert get_odd_collatz(1) == [1]

    def test_n_equals_2(self):
        # Collatz(2) = [2, 1], odd number: 1
        assert get_odd_collatz(2) == [1]

    def test_n_equals_4(self):
        # Collatz(4) = [4, 2, 1], odd number: 1
        assert get_odd_collatz(4) == [1]

    def test_n_equals_8(self):
        # Collatz(8) = [8, 4, 2, 1], odd number: 1
        assert get_odd_collatz(8) == [1]

    def test_n_equals_100(self):
        # Collatz(100) = [100, 50, 25, 76, 38, 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # odd numbers: 25, 19, 29, 11, 17, 13, 5, 1
        assert get_odd_collatz(100) == [1, 5, 11, 13, 17, 19, 25, 29]

    def test_n_equals_1000(self):
        # Larger boundary test
        result = get_odd_collatz(1000)
        # Collatz(1000) = [1000, 500, 250, 125, ...]
        # We verify the result is a list of ints, sorted, and includes 1
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)
        assert 1 in result

    def test_result_is_sorted_increasing(self):
        # For several inputs, verify output is strictly sorted in increasing order
        for n in [1, 2, 3, 5, 7, 10, 12, 20, 27, 100]:
            result = get_odd_collatz(n)
            assert result == sorted(result), f"Result not sorted for n={n}"


class TestGetOddCollatzEdgeInputs:
    """Tests with empty, null, zero-size, or otherwise edge-case inputs."""

    def test_none_input(self):
        # None is not a valid input
        with pytest.raises((TypeError, AttributeError)):
            get_odd_collatz(None)

    def test_string_input(self):
        # String is not a valid input
        with pytest.raises((TypeError, AttributeError)):
            get_odd_collatz("5")

    def test_list_input(self):
        # List is not a valid input
        with pytest.raises((TypeError, AttributeError)):
            get_odd_collatz([5])

    def test_dict_input(self):
        # Dict is not a valid input
        with pytest.raises((TypeError, AttributeError)):
            get_odd_collatz({})


class TestGetOddCollatzProperties:
    """Tests for general properties of the function."""

    def test_result_contains_only_odd_numbers(self):
        # Every element in the result must be odd
        for n in [1, 2, 3, 5, 7, 10, 12, 20, 27, 100, 200, 500]:
            result = get_odd_collatz(n)
            assert all(x % 2 == 1 for x in result), f"Not all odd for n={n}"

    def test_result_contains_one(self):
        # 1 is always in the Collatz sequence, so it must be in the result
        for n in range(1, 101):
            result = get_odd_collatz(n)
            assert 1 in result, f"Missing 1 for n={n}"

    def test_result_contains_n_when_n_is_odd(self):
        # If n is odd, n itself appears in the sequence as the first term
        for n in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 27, 100]:
            if n % 2 == 1:
                result = get_odd_collatz(n)
                assert n in result, f"Missing {n} for n={n}"

    def test_result_does_not_contain_even_numbers(self):
        # No even numbers should appear in the result
        for n in [1, 2, 3, 5, 7, 10, 12, 20, 27, 100]:
            result = get_odd_collatz(n)
            assert all(x % 2 != 0 for x in result), f"Even number found for n={n}"

    def test_single_element_for_power_of_two(self):
        # Powers of 2 have no odd numbers except 1
        for exp in range(1, 10):
            n = 2 ** exp
            result = get_odd_collatz(n)
            assert result == [1], f"Expected [1] for n={n}, got {result}"
