import pytest
from solution import rounded_avg


class TestRoundedAvgBasicCases:
    """Tests based on the examples in the docstring."""

    def test_example_1(self):
        # Average of 1..5 = (1+5)/2 = 3 => bin(3) = "0b11"
        assert rounded_avg(1, 5) == "0b11"

    def test_example_2(self):
        # n > m should return -1
        assert rounded_avg(7, 5) == -1

    def test_example_3(self):
        # Average of 10..20 = (10+20)/2 = 15 => bin(15) = "0b1111"
        assert rounded_avg(10, 20) == "0b1111"

    def test_example_4(self):
        # Average of 20..33 = (20+33)/2 = 26.5 => round to 26 => bin(26) = "0b11010"
        assert rounded_avg(20, 33) == "0b11010"


class TestRoundedAvgEdgeCases:
    """Edge cases around boundaries and special inputs."""

    def test_n_equals_m(self):
        # When n == m, the average is just n itself
        assert rounded_avg(5, 5) == "0b101"

    def test_single_pair_1_1(self):
        assert rounded_avg(1, 1) == "0b1"

    def test_n_greater_than_m(self):
        # Various cases where n > m
        assert rounded_avg(10, 1) == -1
        assert rounded_avg(100, 50) == -1
        assert rounded_avg(2, 1) == -1

    def test_large_values(self):
        # Large positive integers
        result = rounded_avg(1, 1000000)
        expected = round((1 + 1000000) / 2)
        assert result == bin(expected)

    def test_adjacent_numbers(self):
        # Consecutive numbers: average is (n + n+1) / 2 = n + 0.5, rounds to n or n+1
        # Python's round() uses banker's rounding: round(0.5) -> 0, round(1.5) -> 2
        assert rounded_avg(2, 3) == bin(round(2.5))  # round(2.5) = 2 in Python 3
        assert rounded_avg(3, 4) == bin(round(3.5))  # round(3.5) = 4 in Python 3


class TestRoundedAvgReturnType:
    """Tests verifying correct return types."""

    def test_returns_string_on_valid_input(self):
        assert isinstance(rounded_avg(1, 5), str)

    def test_returns_int_on_invalid_input(self):
        assert isinstance(rounded_avg(5, 1), int)

    def test_binary_format_has_prefix(self):
        result = rounded_avg(1, 5)
        assert result.startswith("0b")

    def test_negative_result_is_integer_not_string(self):
        result = rounded_avg(10, 1)
        assert result == -1
        assert isinstance(result, int)


class TestRoundedAvgMathematicalCorrectness:
    """Tests checking mathematical correctness of the average computation."""

    def test_average_of_range_1_to_10(self):
        # Sum of 1..10 = 55, count = 10, avg = 5.5 => round to 6
        # But formula is (1+10)/2 = 5.5 => round to 6
        assert rounded_avg(1, 10) == bin(6)

    def test_average_of_range_1_to_100(self):
        # (1 + 100) / 2 = 50.5 => round to 50 (banker's rounding)
        assert rounded_avg(1, 100) == bin(50)

    def test_even_range_length(self):
        # Range 2..6 has 5 elements: 2,3,4,5,6. Avg = 20/5 = 4
        # Formula: (2+6)/2 = 4
        assert rounded_avg(2, 6) == bin(4)

    def test_odd_range_length(self):
        # Range 1..4 has 4 elements: 1,2,3,4. Avg = 10/4 = 2.5
        # Formula: (1+4)/2 = 2.5 => round to 2 (banker's rounding)
        assert rounded_avg(1, 4) == bin(2)

    def test_all_same_value(self):
        # All values are 42, average is 42
        assert rounded_avg(42, 42) == bin(42)

    def test_very_large_numbers(self):
        # Avoid overflow concerns; Python handles big ints natively
        result = rounded_avg(999999999, 1000000000)
        expected = round((999999999 + 1000000000) / 2)
        assert result == bin(expected)


class TestRoundedAvgBoundaryConditions:
    """Tests at boundary conditions."""

    def test_minimum_positive_inputs(self):
        assert rounded_avg(1, 1) == "0b1"

    def test_one_is_zero_like(self):
        # Smallest possible range
        assert rounded_avg(1, 2) == bin(round(1.5))  # round(1.5) = 2

    def test_rounding_half_cases(self):
        # Verify banker's rounding behavior for .5 cases
        # (1+2)/2 = 1.5 => round to 2
        assert rounded_avg(1, 2) == "0b10"
        # (3+4)/2 = 3.5 => round to 4
        assert rounded_avg(3, 4) == "0b100"
        # (5+6)/2 = 5.5 => round to 6
        assert rounded_avg(5, 6) == "0b110"
