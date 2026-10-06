import pytest
from solution import search


class TestSearchBasicExamples:
    """Tests based on the examples in the docstring."""

    def test_example_1(self):
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        assert search([5, 5, 4, 4, 4]) == -1


class TestSearchSingleElementLists:
    """Tests with lists containing a single element."""

    def test_single_element_matches(self):
        # Value 1 appears once, frequency 1 >= 1 => valid
        assert search([1]) == 1

    def test_single_element_does_not_match(self):
        # Value 5 appears once, frequency 1 < 5 => invalid
        assert search([5]) == -1

    def test_single_large_element(self):
        assert search([100]) == -1


class TestSearchFrequencyEqualsValue:
    """Tests where frequency exactly equals the value."""

    def test_two_twos(self):
        # 2 appears twice, freq 2 >= 2 => valid
        assert search([2, 2]) == 2

    def test_three_threes(self):
        # 3 appears three times, freq 3 >= 3 => valid
        assert search([3, 3, 3]) == 3

    def test_four_fours(self):
        assert search([4, 4, 4, 4]) == 4


class TestSearchFrequencyGreaterThanValue:
    """Tests where frequency exceeds the value."""

    def test_many_ones(self):
        # 1 appears many times, freq > 1 => valid; 1 is the only candidate
        assert search([1, 1, 1, 1]) == 1

    def test_mixed_with_excess_frequency(self):
        # 2 appears 3 times (>= 2), 3 appears 2 times (< 3) => answer is 2
        assert search([2, 2, 2, 3, 3]) == 2


class TestSearchNoValidCandidate:
    """Tests where no element satisfies the condition."""

    def test_all_large_values(self):
        assert search([10, 20, 30]) == -1

    def test_values_larger_than_count(self):
        assert search([6, 6, 6, 6, 6]) == -1  # 5 occurrences < 6

    def test_empty_like_no_match(self):
        assert search([7, 8, 9, 10]) == -1


class TestSearchMultipleCandidates:
    """Tests with multiple elements satisfying the condition."""

    def test_multiple_valid_picks_smallest(self):
        # 1 appears 2 times (>=1), 2 appears 2 times (>=2) => max is 2
        assert search([1, 1, 2, 2]) == 2

    def test_multiple_valid_picks_largest(self):
        # 1 appears 1 time (>=1), 2 appears 2 times (>=2), 3 appears 3 times (>=3)
        assert search([1, 2, 2, 3, 3, 3]) == 3

    def test_complex_multiple_candidates(self):
        # 1: freq 4 >= 1 ✓, 2: freq 3 >= 2 ✓, 3: freq 2 < 3 ✗, 4: freq 1 < 4 ✗
        assert search([1, 1, 1, 1, 2, 2, 2, 3, 3, 4]) == 2


class TestSearchEdgeCases:
    """Additional edge cases."""

    def test_all_same_value_matching(self):
        # 3 appears 5 times, freq 5 >= 3 => valid, returns 3
        assert search([3, 3, 3, 3, 3]) == 3

    def test_list_with_duplicates_of_different_values(self):
        # 1: freq 3 >= 1 ✓, 2: freq 2 >= 2 ✓, 3: freq 1 < 3 ✗
        assert search([1, 1, 1, 2, 2, 3]) == 2

    def test_greatest_valid_is_one(self):
        # Only 1 satisfies the condition
        assert search([1, 1, 5, 5, 5]) == 1  # 1: freq 2>=1✓, 5: freq 3<5✗

    def test_single_occurrence_of_one(self):
        assert search([1, 2, 3]) == 1  # 1: freq 1>=1✓, others fail

    def test_large_list(self):
        lst = [1] * 10 + [2] * 5 + [3] * 3 + [4] * 2 + [5]
        # 1: freq 10>=1✓, 2: freq 5>=2✓, 3: freq 3>=3✓, 4: freq 2<4✗, 5: freq 1<5✗
        assert search(lst) == 3

    def test_all_elements_are_one(self):
        assert search([1, 1, 1, 1, 1]) == 1

    def test_alternating_pattern(self):
        assert search([2, 1, 2, 1, 2, 1]) == 2  # 1: freq 3>=1✓, 2: freq 3>=2✓


class TestSearchReturnNegativeOne:
    """Ensure -1 is returned when appropriate."""

    def test_return_type_on_failure(self):
        result = search([100, 200, 300])
        assert result == -1
        assert isinstance(result, int)

    def test_return_type_on_success(self):
        result = search([1, 2, 2])
        assert result == 2
        assert isinstance(result, int)
