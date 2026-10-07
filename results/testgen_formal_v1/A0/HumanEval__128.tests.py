import pytest
from solution import prod_signs


class TestProdSignsBasicCases:
    """Test the basic examples from the docstring."""

    def test_example_1(self):
        # [1, 2, 2, -4] -> sum(abs) = 9, sign product = -1 => -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_example_2(self):
        # [0, 1] -> contains 0 => 0
        assert prod_signs([0, 1]) == 0

    def test_example_3(self):
        # [] -> empty => None
        assert prod_signs([]) is None


class TestProdSignsEmptyAndZero:
    """Test edge cases involving empty arrays and zeros."""

    def test_empty_list(self):
        assert prod_signs([]) is None

    def test_single_zero(self):
        assert prod_signs([0]) == 0

    def test_multiple_zeros(self):
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_in_middle(self):
        assert prod_signs([1, 0, 2]) == 0

    def test_zero_at_end(self):
        assert prod_signs([1, 2, 0]) == 0

    def test_all_zeros(self):
        assert prod_signs([0, 0]) == 0


class TestProdSignsAllPositive:
    """Test arrays with only positive numbers."""

    def test_single_positive(self):
        assert prod_signs([5]) == 5

    def test_multiple_positives(self):
        # sum(abs) = 1+2+3 = 6, sign product = 1 => 6
        assert prod_signs([1, 2, 3]) == 6

    def test_larger_positives(self):
        # sum(abs) = 10+20+30 = 60, sign product = 1 => 60
        assert prod_signs([10, 20, 30]) == 60

    def test_single_element_one(self):
        assert prod_signs([1]) == 1


class TestProdSignsAllNegative:
    """Test arrays with only negative numbers."""

    def test_single_negative(self):
        # sum(abs) = 5, sign product = -1 => -5
        assert prod_signs([-5]) == -5

    def test_two_negatives(self):
        # sum(abs) = 1+2 = 3, sign product = (-1)*(-1) = 1 => 3
        assert prod_signs([-1, -2]) == 3

    def test_three_negatives(self):
        # sum(abs) = 1+2+3 = 6, sign product = (-1)^3 = -1 => -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_four_negatives(self):
        # sum(abs) = 1+2+3+4 = 10, sign product = (-1)^4 = 1 => 10
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_even_count_negative(self):
        # Even number of negatives => positive result
        assert prod_signs([-3, -7]) == 10

    def test_odd_count_negative(self):
        # Odd number of negatives => negative result
        assert prod_signs([-3, -7, -2]) == -12


class TestProdSignsMixedSigns:
    """Test arrays with a mix of positive and negative numbers."""

    def test_one_negative_others_positive(self):
        # sum(abs) = 1+2+3 = 6, one negative => -6
        assert prod_signs([1, 2, -3]) == -6

    def test_two_negatives_others_positive(self):
        # sum(abs) = 1+2+3+4 = 10, two negatives => +10
        assert prod_signs([1, -2, 3, -4]) == 10

    def test_alternating_signs(self):
        # sum(abs) = 1+1+1+1 = 4, signs: +,-,+,- => product = 1 => 4
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_mixed_with_large_values(self):
        # sum(abs) = 100+200+300 = 600, one negative => -600
        assert prod_signs([100, 200, -300]) == -600

    def test_single_positive_single_negative(self):
        assert prod_signs([5, -3]) == -8

    def test_single_negative_single_positive(self):
        assert prod_signs([-5, 3]) == -8


class TestProdSignsWithZerosAndNegatives:
    """Test combinations of zeros and negative numbers."""

    def test_zero_and_negative(self):
        assert prod_signs([0, -1]) == 0

    def test_zero_negative_positive(self):
        assert prod_signs([0, -1, 2]) == 0

    def test_multiple_zeros_and_negatives(self):
        assert prod_signs([0, -1, -2, 0]) == 0


class TestProdSignsLargeNumbers:
    """Test with larger integer values."""

    def test_large_positive(self):
        assert prod_signs([1000000]) == 1000000

    def test_large_negative(self):
        assert prod_signs([-1000000]) == -1000000

    def test_large_mixed(self):
        # sum(abs) = 1000000 + 2000000 = 3000000, one negative => -3000000
        assert prod_signs([1000000, -2000000]) == -3000000

    def test_many_elements(self):
        arr = list(range(1, 101))
        expected = sum(abs(x) for x in arr)  # all positive => sign product = 1
        assert prod_signs(arr) == expected


class TestProdSignsWithDuplicates:
    """Test arrays with duplicate values."""

    def test_all_same_positive(self):
        assert prod_signs([3, 3, 3]) == 9

    def test_all_same_negative(self):
        assert prod_signs([-3, -3, -3]) == -9

    def test_duplicate_mixed(self):
        assert prod_signs([2, 2, -2, -2]) == 8

    def test_single_value_repeated(self):
        assert prod_signs([5, 5, 5, 5]) == 20


class TestProdSignsReturnTypes:
    """Test that return types are correct."""

    def test_non_empty_returns_int(self):
        assert isinstance(prod_signs([1]), int)

    def test_empty_returns_none(self):
        assert prod_signs([]) is None

    def test_zero_array_returns_int(self):
        assert isinstance(prod_signs([0]), int)

    def test_negative_result_is_int(self):
        assert isinstance(prod_signs([-1]), int)


class TestProdSignsEdgeValues:
    """Test with edge-case numeric values."""

    def test_value_of_one(self):
        assert prod_signs([1, 1, 1]) == 3

    def test_value_of_negative_one(self):
        assert prod_signs([-1, -1, -1]) == -3

    def test_mixed_ones(self):
        # sum(abs) = 3, signs: +,+,- => product = -1 => -3
        assert prod_signs([1, 1, -1]) == -3

    def test_only_zeros(self):
        assert prod_signs([0, 0, 0, 0]) == 0

    def test_single_element_zero(self):
        assert prod_signs([0]) == 0

    def test_single_element_one(self):
        assert prod_signs([1]) == 1

    def test_single_element_negative_one(self):
        assert prod_signs([-1]) == -1
