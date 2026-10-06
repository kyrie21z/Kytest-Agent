import pytest
from solution import solution


class TestSolutionBasicExamples:
    """Test cases from the docstring."""

    def test_example_1(self):
        assert solution([5, 8, 7, 1]) == 12

    def test_example_2(self):
        assert solution([3, 3, 3, 3, 3]) == 9

    def test_example_3(self):
        assert solution([30, 13, 24, 321]) == 0


class TestSolutionSingleElement:
    """Edge case with a single-element list."""

    def test_single_odd_element(self):
        assert solution([7]) == 7

    def test_single_even_element(self):
        assert solution([4]) == 0


class TestSolutionAllOddElements:
    """When all elements are odd."""

    def test_all_odd(self):
        # Indices 0, 2, 4 are even positions -> 1 + 5 + 9 = 15
        assert solution([1, 2, 5, 6, 9]) == 15

    def test_all_odd_alternating(self):
        # All odd, even positions: index 0, 2, 4 -> 3 + 7 + 11 = 21
        assert solution([3, 2, 7, 4, 11]) == 21


class TestSolutionAllEvenElements:
    """When all elements are even — result should always be 0."""

    def test_all_even(self):
        assert solution([2, 4, 6, 8, 10]) == 0

    def test_mixed_with_no_odd_at_even_positions(self):
        # Odd elements only at odd indices
        assert solution([2, 3, 4, 5, 6, 7]) == 0


class TestSolutionNegativeNumbers:
    """Handle negative odd integers."""

    def test_negative_odd_at_even_position(self):
        # Index 0: -3 (odd), Index 2: 5 (odd) -> -3 + 5 = 2
        assert solution([-3, 2, 5, 4]) == 2

    def test_all_negative_odds(self):
        # Index 0: -1, Index 2: -5 -> -1 + (-5) = -6
        assert solution([-1, 2, -5, 4]) == -6

    def test_mixed_positive_and_negative(self):
        # Index 0: -3 (odd), Index 2: 7 (odd), Index 4: -1 (odd) -> -3 + 7 + (-1) = 3
        assert solution([-3, 2, 7, 4, -1, 6]) == 3


class TestSolutionMixedValues:
    """General mixed input scenarios."""

    def test_no_odd_elements(self):
        assert solution([2, 3, 4, 5]) == 0

    def test_only_first_element_is_odd(self):
        assert solution([7, 2, 4, 6]) == 7

    def test_only_last_element_is_odd_at_even_position(self):
        # Index 2 is even position, value 9 is odd
        assert solution([2, 3, 9, 4]) == 9

    def test_large_list(self):
        lst = list(range(1, 21))  # [1, 2, 3, ..., 20]
        # Even indices: 0,2,4,...,18 -> values 1,3,5,...,19 (all odd)
        expected = sum(v for v in range(1, 20, 2))  # 1+3+5+...+19 = 100
        assert solution(lst) == 100

    def test_zeros(self):
        assert solution([0, 0, 0, 0]) == 0

    def test_zero_and_odd(self):
        # Index 0: 0 (even), Index 2: 5 (odd) -> 5
        assert solution([0, 1, 5, 3]) == 5


class TestSolutionReturnTypes:
    """Verify return type is int."""

    def test_returns_int(self):
        result = solution([1, 2, 3])
        assert isinstance(result, int)

    def test_empty_sum_returns_zero(self):
        result = solution([2, 3, 4, 5])
        assert result == 0


class TestSolutionLargeNumbers:
    """Test with large integer values."""

    def test_large_odd_numbers(self):
        assert solution([1000001, 2, 999999, 4]) == 2000000

    def test_mixed_large_values(self):
        lst = [10**9 + 1, 2, 10**9 + 3, 4]
        assert solution(lst) == 2 * (10**9) + 4
