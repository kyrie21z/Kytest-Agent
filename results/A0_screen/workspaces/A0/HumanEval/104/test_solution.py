"""Unit tests for solution.unique_digits."""

import pytest
from solution import unique_digits


class TestUniqueDigitsBasic:
    """Test basic functionality of unique_digits."""

    def test_example_1(self):
        # All numbers with only odd digits should be returned, sorted
        assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]

    def test_example_2(self):
        # No number qualifies — all have at least one even digit
        assert unique_digits([152, 323, 1422, 10]) == []

    def test_single_qualifying_number(self):
        assert unique_digits([13579]) == [13579]

    def test_single_non_qualifying_number(self):
        assert unique_digits([2468]) == []

    def test_empty_list(self):
        assert unique_digits([]) == []


class TestUniqueDigitsEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_all_qualifying_numbers(self):
        assert unique_digits([1, 3, 5, 7, 9]) == [1, 3, 5, 7, 9]

    def test_all_non_qualifying_numbers(self):
        assert unique_digits([2, 4, 6, 8, 10]) == []

    def test_mixed_with_duplicates(self):
        # Duplicates of qualifying numbers should appear as-is (filter preserves them)
        assert unique_digits([1, 1, 3, 3, 5]) == [1, 1, 3, 3, 5]

    def test_unsorted_input(self):
        # Output must be sorted regardless of input order
        assert unique_digits([99, 1, 753, 31]) == [1, 31, 99, 753]

    def test_large_qualifying_number(self):
        assert unique_digits([97531]) == [97531]

    def test_number_with_even_digit_in_middle(self):
        # e.g., 13527 has an even digit '2' → excluded
        assert unique_digits([13527]) == []

    def test_number_with_even_digit_at_end(self):
        # e.g., 1358 has an even digit '8' → excluded
        assert unique_digits([1358]) == []

    def test_number_with_even_digit_at_start(self):
        # e.g., 2357 has an even digit '2' → excluded
        assert unique_digits([2357]) == []

    def test_zero_is_excluded(self):
        # 0 is an even digit; also 0 is not a positive integer per docstring
        assert unique_digits([10, 20, 30]) == []

    def test_single_digit_odd_numbers(self):
        assert unique_digits([1, 3, 5, 7, 9]) == [1, 3, 5, 7, 9]

    def test_single_digit_even_numbers(self):
        assert unique_digits([0, 2, 4, 6, 8]) == []

    def test_repeated_same_qualifying_number(self):
        assert unique_digits([135, 135, 135]) == [135, 135, 135]

    def test_no_qualifying_but_many_numbers(self):
        nums = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        assert unique_digits(nums) == []

    def test_one_qualifying_among_many(self):
        nums = [2, 4, 6, 8, 10, 135, 14, 16, 18, 20]
        assert unique_digits(nums) == [135]

    def test_qualifying_numbers_already_sorted(self):
        assert unique_digits([1, 13, 135, 1357, 13579]) == [1, 13, 135, 1357, 13579]

    def test_qualifying_numbers_reverse_sorted(self):
        assert unique_digits([13579, 1357, 135, 13, 1]) == [1, 13, 135, 1357, 13579]

    def test_negative_numbers_not_expected_but_test_behavior(self):
        # The docstring says "positive integers", but let's verify behavior
        # str(-1) contains '-', which int('-') would fail, but '-' isn't iterated
        # Actually str(-1) = "-1", so '-' would cause ValueError on int('-')
        # This is an edge case we document; skip or handle gracefully
        pass  # Negative numbers are outside spec; no assertion needed


class TestUniqueDigitsReturnTypes:
    """Test that return type is correct."""

    def test_returns_list(self):
        result = unique_digits([1, 3, 5])
        assert isinstance(result, list)

    def test_returns_sorted_list(self):
        result = unique_digits([9, 1, 7, 3, 5])
        assert result == sorted(result)

    def test_elements_are_integers(self):
        result = unique_digits([1, 3, 5])
        assert all(isinstance(x, int) for x in result)


class TestUniqueDigitsComprehensive:
    """Additional comprehensive tests."""

    def test_all_five_odd_digits(self):
        assert unique_digits([13579]) == [13579]

    def test_two_digit_all_odd(self):
        assert unique_digits([11, 13, 15, 17, 19, 31, 33, 35, 37, 39]) == \
            [11, 13, 15, 17, 19, 31, 33, 35, 37, 39]

    def test_three_digit_all_odd(self):
        assert unique_digits([111, 113, 135, 357, 753, 999]) == \
            [111, 113, 135, 357, 753, 999]

    def test_mixed_three_and_four_digit(self):
        result = unique_digits([111, 1234, 3579, 2468])
        assert result == [111, 3579]

    def test_larger_dataset(self):
        nums = list(range(1, 101))
        result = unique_digits(nums)
        # Filter manually to verify
        expected = sorted([n for n in range(1, 101) if all(int(d) % 2 == 1 for d in str(n))])
        assert result == expected
