import pytest
from solution import order_by_points


class TestOrderByPointsBasic:
    """Test basic functionality of order_by_points."""

    def test_empty_list(self):
        assert order_by_points([]) == []

    def test_single_element(self):
        assert order_by_points([5]) == [5]

    def test_two_elements_same_weight(self):
        # 2 and 11 both have digit sum 2; stable sort preserves original order
        # Input [11, 2] => 11 appears first, so it stays first
        assert order_by_points([11, 2]) == [11, 2]

    def test_two_elements_different_weight(self):
        assert order_by_points([10, 2]) == [10, 2]  # 1 < 2

    def test_two_elements_different_weight_reversed(self):
        assert order_by_points([2, 10]) == [10, 2]  # 1 < 2


class TestOrderByPointsPositiveNumbers:
    """Tests with only positive integers."""

    def test_already_sorted(self):
        assert order_by_points([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert order_by_points([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_numbers_with_same_digit_sum(self):
        # 2, 11, 20 all have digit sum 2; stable sort preserves original order
        assert order_by_points([20, 11, 2]) == [20, 11, 2]

    def test_various_positive_numbers(self):
        result = order_by_points([10, 2, 1, 11, 20])
        # weights: 10->1, 2->2, 1->1, 11->2, 20->2
        # sorted by weight: 10(1), 1(1), 2(2), 11(2), 20(2)
        assert result == [10, 1, 2, 11, 20]

    def test_large_numbers(self):
        # 100 -> 1, 99 -> 18, 19 -> 10
        assert order_by_points([99, 19, 100]) == [100, 19, 99]


class TestOrderByPointsNegativeNumbers:
    """Tests with negative integers."""

    def test_single_negative(self):
        assert order_by_points([-5]) == [-5]

    def test_all_negatives(self):
        # -1 -> -1, -11 -> 0, -12 -> 1
        assert order_by_points([-1, -11, -12]) == [-1, -11, -12]

    def test_mixed_negatives_same_weight(self):
        # -2 -> -2, -20 -> -2; stable sort preserves original order
        assert order_by_points([-20, -2]) == [-20, -2]

    def test_example_from_docstring(self):
        assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]

    def test_multi_digit_negative_first_digit_only_negated(self):
        # -101: digits [1,0,1], negate first -> [-1,0,1], sum = 0
        # -11: digits [1,1], negate first -> [-1,1], sum = 0
        # Both have weight 0; stable sort preserves order
        assert order_by_points([-101, -11]) == [-101, -11]

    def test_negative_with_larger_first_digit(self):
        # -99: digits [9,9], negate first -> [-9,9], sum = 0
        # -9: digits [9], negate first -> [-9], sum = -9
        assert order_by_points([-99, -9]) == [-9, -99]


class TestOrderByPointsMixedSigns:
    """Tests with both positive and negative integers."""

    def test_simple_mixed(self):
        assert order_by_points([0, -1, 1]) == [-1, 0, 1]

    def test_zero_handling(self):
        # 0 has digit sum 0
        assert order_by_points([0, 1, -1]) == [-1, 0, 1]

    def test_complex_mixed(self):
        # 3 -> 3, -3 -> -3, 12 -> 3, -12 -> 1
        # weights: 3->3, -3->-3, 12->3, -12->1
        # sorted: -3(-3), -12(1), 3(3), 12(3)
        assert order_by_points([3, 12, -3, -12]) == [-3, -12, 3, 12]

    def test_tie_breaking_preserves_index_order(self):
        # 15 -> 6, 6 -> 6, 24 -> 6; stable sort preserves original order
        assert order_by_points([24, 15, 6]) == [24, 15, 6]


class TestOrderByPointsStability:
    """Tests that stable sorting preserves original relative order."""

    def test_stable_sort_with_duplicates(self):
        # Multiple numbers with same digit sum should maintain relative order
        nums = [2, 11, 20, 101]  # all have digit sum 2
        assert order_by_points(nums) == [2, 11, 20, 101]

    def test_stable_sort_with_negatives(self):
        # -2 -> -2, -11 -> 0, -20 -> -2, -101 -> 0
        # Weights: -2(idx0)->-2, -11(idx1)->0, -20(idx2)->-2, -101(idx3)->0
        # Sorted by weight: -2(-2), -20(-2), -11(0), -101(0)
        assert order_by_points([-2, -11, -20, -101]) == [-2, -20, -11, -101]

    def test_stable_sort_with_positives(self):
        # 15 -> 6, 6 -> 6, 24 -> 6, 51 -> 6
        # All weight 6, stable sort preserves order
        assert order_by_points([15, 6, 24, 51]) == [15, 6, 24, 51]


class TestOrderByPointsEdgeCases:
    """Edge case tests."""

    def test_single_digit_numbers(self):
        assert order_by_points([9, 1, 5, 3]) == [1, 3, 5, 9]

    def test_all_same_number(self):
        assert order_by_points([7, 7, 7]) == [7, 7, 7]

    def test_large_list(self):
        nums = list(range(1, 21))
        result = order_by_points(nums)
        # Verify each element is present
        assert sorted(result) == sorted(nums)
        # Verify length is preserved
        assert len(result) == len(nums)

    def test_numbers_with_many_digits(self):
        # 1000 -> 1, 10000 -> 1, 9999 -> 36
        # Stable sort: 10000 before 1000 in input
        assert order_by_points([9999, 10000, 1000]) == [10000, 1000, 9999]

    def test_negative_with_large_first_digit(self):
        # -9 -> -9, -999 -> 9 (digits [9,9,9], negate first -> [-9,9,9], sum=9)
        assert order_by_points([-999, -9]) == [-9, -999]

    def test_return_type_is_list(self):
        assert isinstance(order_by_points([1, 2]), list)

    def test_original_list_unchanged(self):
        nums = [3, 1, 2]
        original = nums[:]
        order_by_points(nums)
        assert nums == original

    def test_weight_of_zero(self):
        # 0 should have weight 0
        assert order_by_points([0, 1]) == [0, 1]

    def test_weight_of_negative_one(self):
        # -1 has weight -1
        assert order_by_points([-1, 0]) == [-1, 0]

    def test_weight_of_ten(self):
        # 10 has weight 1
        assert order_by_points([10, 1]) == [10, 1]  # both weight 1, stable

    def test_weight_of_hundred(self):
        # 100 has weight 1
        assert order_by_points([100, 1]) == [100, 1]  # both weight 1, stable
