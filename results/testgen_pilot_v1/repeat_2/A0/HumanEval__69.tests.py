import pytest
from solution import search


class TestSearchBasicExamples:
    """Tests using the examples from the docstring."""

    def test_example_1(self):
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        assert search([5, 5, 4, 4, 4]) == -1


class TestSearchSingleElement:
    """Tests with lists containing a single element."""

    def test_single_element_matches(self):
        # [1] -> frequency of 1 is 1, 1 >= 1, so answer is 1
        assert search([1]) == 1

    def test_single_element_does_not_match(self):
        # [2] -> frequency of 2 is 1, 1 < 2, so answer is -1
        assert search([2]) == -1

    def test_single_large_element(self):
        # [100] -> frequency of 100 is 1, 1 < 100, so answer is -1
        assert search([100]) == -1


class TestSearchFrequencyEqualsValue:
    """Tests where frequency exactly equals the value."""

    def test_one_occurrence_of_one(self):
        assert search([1]) == 1

    def test_two_occurrences_of_two(self):
        assert search([2, 2]) == 2

    def test_three_occurrences_of_three(self):
        assert search([3, 3, 3]) == 3

    def test_four_occurrences_of_four(self):
        assert search([4, 4, 4, 4]) == 4


class TestSearchFrequencyGreaterThanValue:
    """Tests where frequency is greater than the value."""

    def test_one_occurs_twice(self):
        # 1 appears 2 times, 2 >= 1, so answer is 1
        assert search([1, 1]) == 1

    def test_one_occurs_many_times(self):
        assert search([1, 1, 1, 1, 1]) == 1

    def test_mixed_frequency_greater(self):
        # 1 appears 3 times (>=1), 2 appears 3 times (>=2)
        # Greatest valid is 2
        assert search([1, 1, 1, 2, 2, 2]) == 2


class TestSearchNoValidElement:
    """Tests where no element satisfies the condition."""

    def test_all_elements_too_large(self):
        # 3 appears 2 times (<3), so no valid element
        assert search([3, 3]) == -1

    def test_all_elements_are_two_but_only_one(self):
        assert search([2]) == -1

    def test_large_values_with_low_frequency(self):
        assert search([10, 20, 30]) == -1

    def test_values_with_insufficient_frequency(self):
        # 6 appears 2 times (<6), 7 appears 3 times (<7)
        assert search([6, 6, 7, 7, 7]) == -1


class TestSearchMultipleCandidates:
    """Tests with multiple elements satisfying the condition."""

    def test_multiple_valid_picks_smallest(self):
        # 1 appears 1 time (>=1), 2 appears 1 time (<2)
        # Only 1 is valid
        assert search([1, 2]) == 1

    def test_multiple_valid_picks_largest(self):
        # 1 appears 1 time (>=1), 2 appears 2 times (>=2), 3 appears 3 times (>=3)
        # All are valid, greatest is 3
        assert search([1, 2, 2, 3, 3, 3]) == 3

    def test_mixed_valid_and_invalid(self):
        # 1 appears 2 times (>=1), 2 appears 2 times (>=2), 3 appears 1 time (<3)
        # Valid: 1 and 2, greatest is 2
        assert search([1, 1, 2, 2, 3]) == 2

    def test_wide_range(self):
        # 1: freq 5 (>=1), 2: freq 4 (>=2), 3: freq 3 (>=3), 4: freq 2 (<4)
        # Valid: 1, 2, 3; greatest is 3
        assert search([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3]) == 3


class TestSearchEdgeCases:
    """Edge case tests."""

    def test_all_same_element_fits(self):
        assert search([5, 5, 5, 5, 5]) == 5

    def test_all_same_element_does_not_fit(self):
        # 5 appears 4 times, 4 < 5
        assert search([5, 5, 5, 5]) == -1

    def test_duplicate_max_value(self):
        # 4 appears 2 times (<4), 3 appears 2 times (<3), 2 appears 2 times (>=2)
        assert search([4, 4, 3, 3, 2, 2]) == 2

    def test_consecutive_numbers(self):
        # 1: freq 1 (>=1), 2: freq 1 (<2), 3: freq 1 (<3)
        assert search([1, 2, 3]) == 1

    def test_large_list(self):
        lst = [1] * 100 + [2] * 50 + [3] * 30
        # 1: freq 100 (>=1), 2: freq 50 (>=2), 3: freq 30 (>=3)
        assert search(lst) == 3

    def test_repeated_pattern(self):
        # [2, 2, 1, 1] -> 2: freq 2 (>=2), 1: freq 2 (>=1), greatest is 2
        assert search([2, 2, 1, 1]) == 2

    def test_alternating_values(self):
        # [1, 2, 1, 2, 1] -> 1: freq 3 (>=1), 2: freq 2 (>=2), greatest is 2
        assert search([1, 2, 1, 2, 1]) == 2


class TestSearchReturnTypes:
    """Tests to ensure correct return type."""

    def test_returns_integer_on_match(self):
        result = search([1, 2, 2])
        assert isinstance(result, int)

    def test_returns_minus_one_when_no_match(self):
        result = search([3, 3, 3])
        assert isinstance(result, int)
        assert result == 3
