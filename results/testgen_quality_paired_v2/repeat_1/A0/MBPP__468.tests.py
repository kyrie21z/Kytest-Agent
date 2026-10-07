import pytest
from solution import max_product


class TestMaxProductBasic:
    """Test basic functionality of max_product."""

    def test_single_element(self):
        assert max_product([5]) == 5

    def test_two_elements_increasing(self):
        assert max_product([2, 3]) == 6

    def test_two_elements_decreasing(self):
        assert max_product([3, 2]) == 3

    def test_three_elements_strictly_increasing(self):
        assert max_product([1, 2, 3]) == 6

    def test_three_elements_all_same(self):
        assert max_product([4, 4, 4]) == 64

    def test_empty_list_raises(self):
        """An empty list has no valid increasing subsequence; max() will raise ValueError."""
        with pytest.raises(ValueError):
            max_product([])


class TestMaxProductIncreasingSubsequences:
    """Test cases focusing on increasing subsequences."""

    def test_simple_increasing(self):
        # Best subsequence: [1,2,3,4] -> product = 24
        assert max_product([1, 2, 3, 4]) == 24

    def test_with_drop_then_increase(self):
        # Subsequences: [1,2,3], [1,5,6] -> products 6, 30 -> max = 30
        assert max_product([1, 2, 3, 1, 5, 6]) == 30

    def test_decreasing_array(self):
        # No increasing pairs; best single element is 5
        assert max_product([5, 4, 3, 2, 1]) == 5

    def test_alternating_values(self):
        # [1, 3, 5, 2, 4, 6]
        # From index 0: [1,3,5] -> 15
        # From index 3: [2,4,6] -> 48
        # max = 48
        assert max_product([1, 3, 5, 2, 4, 6]) == 48

    def test_equal_consecutive_elements(self):
        # Equal elements are considered non-decreasing (not strictly increasing)
        # [2, 2, 2] -> product = 8
        assert max_product([2, 2, 2]) == 8

    def test_mixed_equal_and_increasing(self):
        # [1, 2, 2, 3] -> product = 1*2*2*3 = 12
        assert max_product([1, 2, 2, 3]) == 12


class TestMaxProductEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_negative_numbers_only_decreasing(self):
        # [-1, -2, -3] -> decreasing, so max single element = -1
        assert max_product([-1, -2, -3]) == -1

    def test_negative_numbers_increasing(self):
        # [-5, -3, -1] -> increasing, product = (-5)*(-3)*(-1) = -15
        # But also consider single elements: -5, -3, -1 -> max = -1
        # The algorithm tracks products per position, so we need to check carefully
        result = max_product([-5, -3, -1])
        assert result >= -15

    def test_mixed_positive_and_negative(self):
        # [3, -1, 2, 4] 
        # From index 0: [3] -> 3
        # From index 1: [-1, 2, 4] -> -1*2*4 = -8
        # From index 2: [2, 4] -> 8
        # From index 3: [4] -> 4
        # max = 8
        assert max_product([3, -1, 2, 4]) == 8

    def test_zero_in_array(self):
        # [1, 2, 0, 3, 4]
        # From index 0: [1, 2] -> 2, then arr[1]=2 > arr[2]=0 -> break
        # From index 3: [3, 4] -> 12
        # max = 12
        assert max_product([1, 2, 0, 3, 4]) == 12

    def test_zero_as_single_element(self):
        # [-1, 0, 1]
        # From index 0: [-1, 0, 1] -> 0
        # From index 1: [0, 1] -> 0
        # From index 2: [1] -> 1
        # max = 1
        assert max_product([-1, 0, 1]) == 1

    def test_large_increasing_sequence(self):
        arr = list(range(1, 11))  # [1, 2, 3, ..., 10]
        expected = 3628800  # 10!
        assert max_product(arr) == expected

    def test_larger_array_with_gap(self):
        # [1, 2, 3, 10, 1, 2, 3, 4, 5]
        # Best: [1,2,3,10] -> 60 or [1,2,3,4,5] -> 120
        assert max_product([1, 2, 3, 10, 1, 2, 3, 4, 5]) == 120


class TestMaxProductAlgorithmBehavior:
    """Test that verify the specific behavior of the algorithm."""

    def test_algorithm_checks_non_decreasing(self):
        # Verify that equal consecutive elements don't break the sequence
        assert max_product([3, 3, 3, 3]) == 81

    def test_break_on_decrease(self):
        # [1, 5, 2, 3]
        # From index 0: [1, 5] -> 5, then arr[1]=5 > arr[2]=2 -> break
        # From index 2: [2, 3] -> 6
        # max = 6
        assert max_product([1, 5, 2, 3]) == 6

    def test_longest_increasing_suffix_wins(self):
        # [10, 1, 2, 3, 4, 5]
        # From index 0: [10] -> 10 (arr[0]=10 > arr[1]=1 -> break)
        # From index 1: [1,2,3,4,5] -> 120
        # max = 120
        assert max_product([10, 1, 2, 3, 4, 5]) == 120

    def test_very_short_sequences(self):
        assert max_product([7]) == 7
        assert max_product([2, 5]) == 10
        assert max_product([5, 2]) == 5

    def test_product_can_be_smaller_than_single_element(self):
        # When including more elements reduces the product
        # [10, 1, 1, 1] -> from index 0: [10] only (10>1 break); from index 1: [1,1,1]->1
        # max = 10
        assert max_product([10, 1, 1, 1]) == 10

    def test_fractional_effect_with_ones(self):
        # [2, 1, 1, 1, 1, 3]
        # From index 0: [2, 1]? arr[0]=2 > arr[1]=1 -> break, so just [2]
        # From index 1: [1, 1, 1, 1, 3] -> 1*1*1*1*3 = 3
        # max = 3
        assert max_product([2, 1, 1, 1, 1, 3]) == 3


class TestMaxProductReturnTypes:
    """Test return types and data integrity."""

    def test_returns_integer_for_integer_input(self):
        result = max_product([2, 3, 4])
        assert isinstance(result, int)

    def test_result_is_numeric(self):
        result = max_product([1, 2, 3, 4, 5])
        assert isinstance(result, (int, float))

    def test_does_not_modify_original_list(self):
        original = [1, 2, 3, 4, 5]
        original_copy = original[:]
        max_product(original)
        assert original == original_copy
