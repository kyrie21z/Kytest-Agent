import pytest
from solution import minSubArraySum


class TestMinSubArraySum:
    """Tests for the minSubArraySum function."""

    # --- Docstring examples ---

    def test_example_1(self):
        assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1

    def test_example_2(self):
        assert minSubArraySum([-1, -2, -3]) == -6

    # --- Single element arrays ---

    def test_single_positive(self):
        assert minSubArraySum([5]) == 5

    def test_single_negative(self):
        assert minSubArraySum([-5]) == -5

    def test_single_zero(self):
        assert minSubArraySum([0]) == 0

    # --- All positive numbers ---

    def test_all_positive(self):
        assert minSubArraySum([1, 2, 3, 4, 5]) == 1

    def test_all_positive_unsorted(self):
        assert minSubArraySum([5, 1, 3, 2, 4]) == 1

    # --- All negative numbers ---

    def test_all_negative(self):
        assert minSubArraySum([-3, -1, -4, -2]) == -10

    def test_all_negative_two_elements(self):
        assert minSubArraySum([-2, -3]) == -5

    # --- Mixed positive and negative numbers ---

    def test_mixed_basic(self):
        assert minSubArraySum([1, -2, 3, -4, 5]) == -4

    def test_mixed_with_larger_negative_subarray(self):
        assert minSubArraySum([2, -5, 3, -1]) == -5

    def test_mixed_negative_at_start(self):
        assert minSubArraySum([-3, 1, 2]) == -3

    def test_mixed_negative_at_end(self):
        assert minSubArraySum([1, 2, -4]) == -4

    def test_mixed_alternating(self):
        assert minSubArraySum([1, -1, 1, -1, 1]) == -1

    def test_mixed_deep_negative(self):
        assert minSubArraySum([3, -10, 5, -2, 1]) == -10

    # --- Arrays containing zeros ---

    def test_zeros_and_positives(self):
        assert minSubArraySum([0, 1, 2]) == 0

    def test_zeros_and_negatives(self):
        assert minSubArraySum([-1, 0, -2]) == -3

    def test_all_zeros(self):
        assert minSubArraySum([0, 0, 0]) == 0

    def test_zero_in_middle(self):
        assert minSubArraySum([1, 0, -3, 2]) == -3

    # --- Two element arrays ---

    def test_two_both_positive(self):
        assert minSubArraySum([3, 5]) == 3

    def test_two_both_negative(self):
        assert minSubArraySum([-3, -5]) == -8

    def test_two_one_each(self):
        assert minSubArraySum([5, -3]) == -3

    def test_two_reversed(self):
        assert minSubArraySum([-3, 5]) == -3

    # --- Larger arrays ---

    def test_large_all_negative(self):
        nums = list(range(-10, 0))
        assert minSubArraySum(nums) == -55

    def test_large_mixed(self):
        nums = [i % 3 - 1 for i in range(100)]
        assert minSubArraySum(nums) == -1

    def test_large_single_min(self):
        nums = [1] * 100 + [-999] + [1] * 100
        assert minSubArraySum(nums) == -999

    # --- Edge cases ---

    def test_equal_elements(self):
        assert minSubArraySum([7, 7, 7, 7]) == 7

    def test_equal_negative_elements(self):
        assert minSubArraySum([-4, -4, -4]) == -12

    def test_two_element_same_value(self):
        assert minSubArraySum([3, 3]) == 3

    def test_cumulative_negative(self):
        # Minimum subarray is [-2, -3, -4] with sum -9
        assert minSubArraySum([1, -2, -3, -4]) == -9

    def test_partial_recovery(self):
        # Sum goes negative then recovers partially
        assert minSubArraySum([5, -10, 3, -2]) == -10

    def test_negative_then_positive_total(self):
        assert minSubArraySum([-5, 10, -3]) == -5

    def test_wide_range_values(self):
        assert minSubArraySum([1000000, -2000000, 1000000]) == -2000000

    def test_very_small_negative(self):
        assert minSubArraySum([-1, -1, -1, -1, -1]) == -5

    def test_positive_then_negative_subarray(self):
        assert minSubArraySum([10, 20, -50, 5, 10]) == -50
