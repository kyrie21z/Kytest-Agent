import pytest
from solution import search


class TestSearch:
    """Tests for the search function."""

    def test_example_1(self):
        """Test case from docstring: [4, 1, 2, 2, 3, 1] == 2"""
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        """Test case from docstring: [1, 2, 2, 3, 3, 3, 4, 4, 4] == 3"""
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        """Test case from docstring: [5, 5, 4, 4, 4] == -1"""
        assert search([5, 5, 4, 4, 4]) == -1

    def test_single_element_matches(self):
        """Single element where frequency equals value."""
        assert search([1]) == 1

    def test_single_element_no_match(self):
        """Single element where frequency is less than value."""
        assert search([5]) == -1

    def test_all_same_elements(self):
        """All elements are the same; check if count >= value."""
        # [3, 3, 3] -> freq=3, value=3 => 3 >= 3 => return 3
        assert search([3, 3, 3]) == 3

    def test_all_same_elements_freq_less_than_value(self):
        """All elements same but frequency < value."""
        # [5, 5] -> freq=2, value=5 => 2 < 5 => return -1
        assert search([5, 5]) == -1

    def test_multiple_candidates_returns_greatest(self):
        """When multiple values satisfy condition, return the greatest."""
        # 2 appears 3 times (3>=2), 3 appears 3 times (3>=3) => max(2,3)=3
        assert search([2, 2, 2, 3, 3, 3]) == 3

    def test_larger_value_with_higher_frequency(self):
        """Larger value has higher frequency and should be returned."""
        # 4 appears 4 times (4>=4) => return 4
        assert search([1, 2, 2, 3, 3, 4, 4, 4, 4]) == 4

    def test_smaller_value_satisfies_but_larger_does_not(self):
        """Only smaller value satisfies the condition."""
        # 1 appears 5 times (5>=1), 2 appears 1 time (1<2) => return 1
        assert search([1, 1, 1, 1, 1, 2]) == 1

    def test_two_elements_equal_to_value(self):
        """Edge case: list with two identical elements equal to their value."""
        # [2, 2] -> freq=2, value=2 => 2 >= 2 => return 2
        assert search([2, 2]) == 2

    def test_many_duplicates_of_small_number(self):
        """Small number with very high frequency."""
        # 1 appears 100 times => return 1
        assert search([1] * 100) == 1

    def test_mixed_with_non_qualifying_large_numbers(self):
        """Large numbers that don't qualify mixed with qualifying ones."""
        # 2 appears 2 times (2>=2), 100 appears 1 time (1<100) => return 2
        assert search([2, 2, 100]) == 2

    def test_values_equal_to_frequency(self):
        """Values exactly equal to their frequency."""
        # 3 appears 3 times => return 3
        assert search([3, 3, 3]) == 3

    def test_frequency_greater_than_value(self):
        """Frequency strictly greater than value."""
        # 1 appears 5 times (5>1) => return 1
        assert search([1, 1, 1, 1, 1]) == 1

    def test_result_is_int(self):
        """Ensure return type is always int."""
        assert isinstance(search([1]), int)
        assert isinstance(search([5, 5, 5]), int)

    def test_return_type_negative_one(self):
        """Return -1 as integer when no match found."""
        result = search([10, 20, 30])
        assert result == -1
        assert isinstance(result, int)

    def test_unsorted_input(self):
        """Function should work regardless of input order."""
        # 1 appears 3 times (3>=1), 2 appears 4 times (4>=2), 3 appears 3 times (3>=3)
        # All qualify, max is 3
        assert search([3, 1, 2, 3, 1, 2, 2, 3, 1, 2]) == 3

    def test_all_unique_elements(self):
        """All unique elements; each has frequency 1."""
        # Only 1 qualifies (freq 1 >= value 1); others have freq 1 < value
        assert search([1, 2, 3, 4, 5]) == 1

    def test_large_list(self):
        """Test with a larger list to ensure correctness at scale."""
        lst = [i for i in range(1, 11)] * 10
        # Each number 1-10 appears 10 times
        # 1: 10>=1 yes, 2: 10>=2 yes, ..., 10: 10>=10 yes => max=10
        assert search(lst) == 10

    def test_no_element_satisfies(self):
        """No element has frequency >= its value."""
        assert search([10, 20, 30, 40, 50]) == -1
