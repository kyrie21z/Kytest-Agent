import pytest
from solution import search


class TestSearchBasicCases:
    """Tests based on the examples provided in the docstring."""

    def test_example_1(self):
        """[4, 1, 2, 2, 3, 1] -> 2 (freq of 2 is 2, freq of 1 is 2)"""
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        """[1, 2, 2, 3, 3, 3, 4, 4, 4] -> 3 (freq of 3 is 3, freq of 4 is 3 but 4 > 3 so fails)"""
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        """[5, 5, 4, 4, 4] -> -1 (no element satisfies freq >= value)"""
        assert search([5, 5, 4, 4, 4]) == -1


class TestSearchSingleElementLists:
    """Tests with lists containing a single element."""

    def test_single_element_one(self):
        """[1] -> 1 (freq of 1 is 1, 1 >= 1)"""
        assert search([1]) == 1

    def test_single_element_greater_than_one(self):
        """[5] -> -1 (freq of 5 is 1, 1 < 5)"""
        assert search([5]) == -1

    def test_single_element_two(self):
        """[2] -> -1 (freq of 2 is 1, 1 < 2)"""
        assert search([2]) == -1


class TestSearchEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_list_not_expected_but_handled(self):
        """Function expects non-empty list; skip or document behavior."""
        # Per docstring, input is non-empty, so we don't test empty list.

    def test_all_same_elements_satisfy_condition(self):
        """[2, 2, 2] -> 2 (freq of 2 is 3, 3 >= 2)"""
        assert search([2, 2, 2]) == 2

    def test_all_same_elements_dont_satisfy_condition(self):
        """[5, 5, 5] -> -1 (freq of 5 is 3, 3 < 5)"""
        assert search([5, 5, 5]) == -1

    def test_frequency_equals_value(self):
        """[3, 3, 3] -> 3 (freq of 3 is exactly 3)"""
        assert search([3, 3, 3]) == 3

    def test_frequency_greater_than_value(self):
        """[1, 1, 1, 1] -> 1 (freq of 1 is 4, 4 >= 1)"""
        assert search([1, 1, 1, 1]) == 1

    def test_multiple_candidates_returns_greatest(self):
        """[1, 1, 2, 2, 3, 3, 3] -> 3 (all satisfy, 3 is greatest)"""
        assert search([1, 1, 2, 2, 3, 3, 3]) == 3

    def test_larger_candidate_fails_smaller_passes(self):
        """[1, 1, 1, 10, 10] -> 1 (10 has freq 2 < 10, only 1 qualifies)"""
        assert search([1, 1, 1, 10, 10]) == 1


class TestSearchWithLargeValues:
    """Tests involving large integer values."""

    def test_large_value_with_high_frequency(self):
        """A large number repeated enough times to satisfy condition."""
        lst = [100] * 100
        assert search(lst) == 100

    def test_large_value_with_insufficient_frequency(self):
        """A large number not repeated enough times."""
        lst = [100] * 50 + [1] * 100
        # 100 has freq 50 < 100 (fails), 1 has freq 100 >= 1 (passes)
        assert search(lst) == 1

    def test_mixed_large_and_small(self):
        """Mix of large failing and small passing values."""
        lst = [50, 50] + [1] * 10
        assert search(lst) == 1  # 50 has freq 2 < 50, 1 has freq 10 >= 1


class TestSearchWithDuplicates:
    """Tests focusing on duplicate handling."""

    def test_many_duplicates_of_one(self):
        """[1, 1, 1, 1, 1] -> 1"""
        assert search([1, 1, 1, 1, 1]) == 1

    def test_no_duplicates_at_all(self):
        """[1, 2, 3] -> 1 (only 1 has freq 1 >= 1)"""
        assert search([1, 2, 3]) == 1

    def test_no_duplicates_except_one(self):
        """[1, 2, 2, 3, 4] -> 2 (2 has freq 2 >= 2)"""
        assert search([1, 2, 2, 3, 4]) == 2

    def test_only_one_qualifies_among_duplicates(self):
        """[1, 2, 2, 3, 3, 3, 4, 4, 4, 4] -> 4 (4 has freq 4 >= 4)"""
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == 4


class TestSearchReturnNegativeOne:
    """Tests where the expected return value is -1."""

    def test_all_values_exceed_frequency(self):
        """[2, 3, 4, 5] -> -1 (each appears once, all values > 1)"""
        assert search([2, 3, 4, 5]) == -1

    def test_values_equal_to_frequency_but_none_qualify(self):
        """[2, 2, 3, 3, 3] -> 3 (3 has freq 3 >= 3)"""
        assert search([2, 2, 3, 3, 3]) == 3

    def test_truly_no_qualifying_element(self):
        """[6, 7, 8, 9, 10] -> -1"""
        assert search([6, 7, 8, 9, 10]) == -1


class TestSearchTypeAndInputValidation:
    """Tests for input type considerations."""

    def test_sorted_input(self):
        """[1, 1, 2, 2, 2, 3, 3, 3] -> 3"""
        assert search([1, 1, 2, 2, 2, 3, 3, 3]) == 3

    def test_unsorted_input(self):
        """Unsorted version of same data should give same result."""
        assert search([3, 1, 2, 3, 1, 2, 3, 2]) == 3

    def test_reverse_sorted_input(self):
        """Reverse sorted list: [3,3,2,2,1,1] -> 2 (3 has freq 2 < 3, 2 has freq 2 >= 2)"""
        assert search([3, 3, 2, 2, 1, 1]) == 2

    def test_widely_spaced_values(self):
        """Values spread across range."""
        assert search([1, 50, 100, 1, 1, 1, 1, 1]) == 1


class TestSearchPerformance:
    """Tests that exercise larger inputs."""

    def test_medium_list(self):
        """A moderately sized list."""
        lst = list(range(1, 101)) * 10  # Each number 1-100 appears 10 times
        # Only numbers <= 10 qualify (freq 10 >= value). Greatest is 10.
        assert search(lst) == 10

    def test_repeated_small_values(self):
        """Many repetitions of small values."""
        lst = [1, 2] * 1000
        # 1 has freq 1000 >= 1, 2 has freq 1000 >= 2. Greatest is 2.
        assert search(lst) == 2
