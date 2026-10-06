import pytest
from solution import search


class TestSearchBasicCases:
    """Tests based on the examples given in the docstring."""

    def test_example_1(self):
        assert search([4, 1, 2, 2, 3, 1]) == 2

    def test_example_2(self):
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

    def test_example_3(self):
        assert search([5, 5, 4, 4, 4]) == -1


class TestSearchSingleElement:
    """Tests with single-element lists."""

    def test_single_element_matches(self):
        # [1] -> frequency of 1 is 1, which is >= 1, so return 1
        assert search([1]) == 1

    def test_single_element_no_match(self):
        # [2] -> frequency of 2 is 1, which is < 2, so return -1
        assert search([2]) == -1

    def test_large_single_element(self):
        # [100] -> frequency of 100 is 1, which is < 100, so return -1
        assert search([100]) == -1


class TestSearchFrequencyEqualsValue:
    """Tests where frequency exactly equals the value."""

    def test_value_1_freq_1(self):
        assert search([1]) == 1

    def test_value_2_freq_2(self):
        # [2, 2] -> freq of 2 is 2 >= 2, return 2
        assert search([2, 2]) == 2

    def test_value_3_freq_3(self):
        # [3, 3, 3] -> freq of 3 is 3 >= 3, return 3
        assert search([3, 3, 3]) == 3

    def test_value_4_freq_4(self):
        # [4, 4, 4, 4] -> freq of 4 is 4 >= 4, return 4
        assert search([4, 4, 4, 4]) == 4


class TestSearchFrequencyGreaterThanOrEqual:
    """Tests where frequency is strictly greater than the value."""

    def test_value_1_freq_5(self):
        # [1, 1, 1, 1, 1] -> freq of 1 is 5 >= 1, return 1
        assert search([1, 1, 1, 1, 1]) == 1

    def test_value_2_freq_5(self):
        # [2, 2, 2, 2, 2] -> freq of 2 is 5 >= 2, return 2
        assert search([2, 2, 2, 2, 2]) == 2

    def test_mixed_freq_greater(self):
        # [1, 1, 1, 2, 2, 2, 2, 2] -> 1 has freq 3>=1, 2 has freq 5>=2, max is 2
        assert search([1, 1, 1, 2, 2, 2, 2, 2]) == 2


class TestSearchNoValidElement:
    """Tests where no element satisfies the condition."""

    def test_all_elements_too_large(self):
        # [3, 3, 3] -> freq of 3 is 3 >= 3, actually valid! So this won't be -1
        pass  # Handled above

    def test_all_elements_frequency_less_than_value(self):
        # [3, 4, 5] -> each appears once, all < their value
        assert search([3, 4, 5]) == -1

    def test_large_values_with_low_frequency(self):
        # [10, 20, 30] -> each appears once, all < their value
        assert search([10, 20, 30]) == -1

    def test_two_elements_each_appearing_once(self):
        assert search([7, 8]) == -1


class TestSearchMultipleCandidates:
    """Tests where multiple elements satisfy the condition; should return the greatest."""

    def test_multiple_valid_return_greatest(self):
        # [1, 1, 1, 2, 2, 3, 3, 3] -> 1:freq3>=1, 2:freq2>=2, 3:freq3>=3, max=3
        assert search([1, 1, 1, 2, 2, 3, 3, 3]) == 3

    def test_smaller_value_has_higher_freq_but_larger_valid_exists(self):
        # [1]*10 + [2]*2 -> 1:freq10>=1, 2:freq2>=2, max=2
        assert search([1] * 10 + [2, 2]) == 2

    def test_larger_value_has_lower_freq_and_is_invalid(self):
        # [1]*5 + [3] -> 1:freq5>=1(valid), 3:freq1<3(invalid), max=1
        assert search([1] * 5 + [3]) == 1

    def test_mixed_valid_and_invalid(self):
        # [2, 2, 2, 5, 5] -> 2:freq3>=2(valid), 5:freq2<5(invalid), max=2
        assert search([2, 2, 2, 5, 5]) == 2


class TestSearchEdgeCases:
    """Edge case tests."""

    def test_list_of_ones(self):
        # All ones, freq=len(lst) >= 1 always
        assert search([1, 1, 1, 1, 1]) == 1

    def test_alternating_pattern(self):
        # [1, 2, 1, 2, 1, 2] -> 1:freq3>=1, 2:freq3>=2, max=2
        assert search([1, 2, 1, 2, 1, 2]) == 2

    def test_consecutive_duplicates(self):
        # [1, 2, 2, 3, 3, 3, 4, 4, 4, 4] -> 1:1>=1, 2:2>=2, 3:3>=3, 4:4>=4, max=4
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == 4

    def test_only_twos(self):
        # [2, 2, 2, 2] -> 2:freq4>=2, return 2
        assert search([2, 2, 2, 2]) == 2

    def test_three_fours(self):
        # [4, 4, 4] -> 4:freq3<4, return -1
        assert search([4, 4, 4]) == -1

    def test_four_fives(self):
        # [5, 5, 5, 5] -> 5:freq4<5, return -1
        assert search([5, 5, 5, 5]) == -1

    def test_five_sixes(self):
        # [6, 6, 6, 6, 6] -> 6:freq5<6, return -1
        assert search([6, 6, 6, 6, 6]) == -1

    def test_one_with_others(self):
        # [1, 100, 100] -> 1:freq2>=1(valid), 100:freq2<100(invalid), max=1
        assert search([1, 100, 100]) == 1


class TestSearchLargeValues:
    """Tests with large integer values."""

    def test_large_value_with_enough_frequency(self):
        # 100 appearing 100 times -> freq 100 >= 100, return 100
        assert search([100] * 100) == 100

    def test_large_value_without_enough_frequency(self):
        # 100 appearing 99 times -> freq 99 < 100, return -1
        assert search([100] * 99) == -1

    def test_mixed_large_and_small(self):
        # [1]*10 + [100]*100 -> 1:freq10>=1, 100:freq100>=100, max=100
        assert search([1] * 10 + [100] * 100) == 100

    def test_large_value_bigger_than_freq(self):
        # [50]*25 -> 50:freq25<50, return -1
        assert search([50] * 25) == -1


class TestSearchReturnTypes:
    """Tests to verify return type consistency."""

    def test_returns_integer_on_valid(self):
        result = search([2, 2])
        assert isinstance(result, int)

    def test_returns_minus_one_as_integer(self):
        result = search([5, 5, 5])
        assert isinstance(result, int)
        assert result == -1
