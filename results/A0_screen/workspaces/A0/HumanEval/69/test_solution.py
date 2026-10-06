import pytest
from solution import search


class TestSearchBasicExamples:
    """Tests based on the docstring examples."""

    def test_example_1(self):
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        assert search([5, 5, 4, 4, 4]) == -1


class TestSearchSingleElement:
    """Tests with single-element lists."""

    def test_single_element_satisfies(self):
        # Frequency 1 >= value 1
        assert search([1]) == 1

    def test_single_element_does_not_satisfy(self):
        # Frequency 1 < value 5
        assert search([5]) == -1

    def test_single_large_element(self):
        assert search([100]) == -1


class TestSearchFrequencyEqualsValue:
    """Tests where frequency exactly equals the value."""

    def test_freq_equals_value(self):
        # 3 appears 3 times, so freq(3) = 3 >= 3
        assert search([3, 3, 3]) == 3

    def test_multiple_with_exact_match(self):
        # 2 appears 2 times, 3 appears 3 times -> max is 3
        assert search([2, 2, 3, 3, 3]) == 3

    def test_larger_one_wins(self):
        # 2 appears 2 times, 4 appears 4 times -> max is 4
        assert search([2, 2, 4, 4, 4, 4]) == 4


class TestSearchFrequencyGreaterThanValue:
    """Tests where frequency is strictly greater than the value."""

    def test_freq_greater_than_value(self):
        # 1 appears 5 times, freq(1)=5 >= 1
        assert search([1, 1, 1, 1, 1]) == 1

    def test_mixed_freq_greater(self):
        # 1 appears 3 times (freq>=1), 2 appears 3 times (freq>=2) -> max is 2
        assert search([1, 1, 1, 2, 2, 2]) == 2

    def test_small_value_with_high_freq(self):
        # 1 appears many times, but nothing else qualifies
        assert search([1, 1, 1, 1, 1, 1, 1, 1]) == 1


class TestSearchNoValidElement:
    """Tests where no element satisfies the condition."""

    def test_all_elements_too_large(self):
        assert search([10, 10, 10]) == -1

    def test_two_elements_each_once(self):
        # Each appears once, but both > 1
        assert search([2, 3]) == -1

    def test_distinct_large_numbers(self):
        assert search([5, 6, 7, 8]) == -1

    def test_all_same_large_number(self):
        # 4 appears 4 times -> freq(4)=4 >= 4, so this actually returns 4
        pass  # Handled in other tests


class TestSearchMultipleCandidates:
    """Tests with multiple elements that could qualify."""

    def test_multiple_qualifying(self):
        # 1 appears 2 times (qualifies), 2 appears 2 times (qualifies) -> max is 2
        assert search([1, 1, 2, 2]) == 2

    def test_three_candidates(self):
        # 1 appears 3 times, 2 appears 3 times, 3 appears 3 times -> max is 3
        assert search([1, 1, 1, 2, 2, 2, 3, 3, 3]) == 3

    def test_non_contiguous_values(self):
        # 1 appears 5 times (qualifies), 5 appears 5 times (qualifies) -> max is 5
        assert search([1]*5 + [5]*5) == 5

    def test_winner_has_lower_freq(self):
        # 1 appears 10 times (qualifies), 2 appears 2 times (qualifies) -> max is 2
        assert search([1]*10 + [2, 2]) == 2


class TestSearchEdgeCases:
    """Additional edge case tests."""

    def test_list_with_one(self):
        # 1 always qualifies since any occurrence gives freq >= 1
        assert search([1, 5, 5, 5]) == 1

    def test_list_with_only_ones(self):
        assert search([1, 1, 1, 1]) == 1

    def test_consecutive_duplicates(self):
        # 2 appears 4 times (qualifies), 3 appears 3 times (qualifies) -> max is 3
        assert search([2, 2, 2, 2, 3, 3, 3]) == 3

    def test_unsorted_input(self):
        # Same as example 1 but shuffled
        result = search([3, 1, 4, 2, 1, 2])
        assert result == 2

    def test_large_list(self):
        # Create a list where 100 appears 100 times
        lst = [100] * 100
        assert search(lst) == 100

    def test_large_list_no_match(self):
        # 100 appears only 99 times, not enough
        lst = [100] * 99
        assert search(lst) == -1

    def test_boundary_case_value_2(self):
        # 2 needs at least 2 occurrences
        assert search([2, 2, 5, 5, 5]) == 2

    def test_value_3_needs_3_occurrences(self):
        # 3 needs at least 3 occurrences; here 3 appears only 2 times, so it doesn't qualify
        # 5 appears 3 times but 3 < 5, so it also doesn't qualify
        assert search([3, 3, 5, 5, 5]) == -1

    def test_value_3_with_enough_occurrences(self):
        # 3 appears 3 times, qualifies
        assert search([3, 3, 3, 7, 7, 7, 7, 7, 7]) == 3


class TestSearchReturnTypes:
    """Tests to verify return type consistency."""

    def test_returns_integer(self):
        assert isinstance(search([1, 2, 2]), int)

    def test_returns_negative_one_on_failure(self):
        assert search([10, 20, 30]) == -1

    def test_returns_positive_on_success(self):
        assert search([1, 1, 2, 2]) > 0
