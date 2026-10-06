import pytest
from solution import common


class TestCommonBasic:
    """Test basic functionality of the common function."""

    def test_example_from_docstring(self):
        result = common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121])
        assert result == [1, 5, 653]

    def test_example_2_from_docstring(self):
        result = common([5, 3, 2, 8], [3, 2])
        assert result == [2, 3]

    def test_no_common_elements(self):
        result = common([1, 2, 3], [4, 5, 6])
        assert result == []

    def test_single_common_element(self):
        result = common([1, 2, 3], [3, 4, 5])
        assert result == [3]

    def test_all_elements_common(self):
        result = common([1, 2, 3], [1, 2, 3])
        assert result == [1, 2, 3]

    def test_one_list_empty(self):
        result = common([], [1, 2, 3])
        assert result == []

    def test_both_lists_empty(self):
        result = common([], [])
        assert result == []

    def test_other_list_empty(self):
        result = common([1, 2, 3], [])
        assert result == []


class TestCommonDuplicates:
    """Test behavior with duplicate elements."""

    def test_duplicates_in_first_list(self):
        result = common([1, 1, 2, 2, 3], [2, 3])
        assert result == [2, 3]

    def test_duplicates_in_second_list(self):
        result = common([1, 2, 3], [2, 2, 3, 3])
        assert result == [2, 3]

    def test_duplicates_in_both_lists(self):
        result = common([1, 1, 2, 2], [2, 2, 3, 3])
        assert result == [2]

    def test_all_same_elements(self):
        result = common([5, 5, 5, 5], [5, 5, 5])
        assert result == [5]


class TestCommonNegativeNumbers:
    """Test behavior with negative numbers."""

    def test_negative_numbers(self):
        result = common([-1, -2, -3], [-2, -3, -4])
        assert result == [-3, -2]

    def test_mixed_positive_and_negative(self):
        result = common([-1, 0, 1], [0, 1, 2])
        assert result == [0, 1]

    def test_only_negative_common(self):
        result = common([-5, -3, -1], [-3, -2, -1])
        assert result == [-3, -1]


class TestCommonEdgeCases:
    """Test edge cases and special scenarios."""

    def test_single_element_lists_same(self):
        result = common([42], [42])
        assert result == [42]

    def test_single_element_lists_different(self):
        result = common([1], [2])
        assert result == []

    def test_large_overlap(self):
        l1 = list(range(100))
        l2 = list(range(50, 150))
        result = common(l1, l2)
        assert result == list(range(50, 100))

    def test_no_overlap_large_lists(self):
        l1 = list(range(100))
        l2 = list(range(100, 200))
        result = common(l1, l2)
        assert result == []

    def test_unsorted_input(self):
        result = common([3, 1, 2], [2, 1, 3])
        assert result == [1, 2, 3]

    def test_result_is_sorted(self):
        result = common([9, 1, 5, 3], [3, 5, 1, 9])
        assert result == sorted(result)


class TestCommonTypes:
    """Test with different data types."""

    def test_strings(self):
        result = common(["apple", "banana", "cherry"], ["banana", "date"])
        assert result == ["banana"]

    def test_floats(self):
        result = common([1.5, 2.5, 3.5], [2.5, 3.5, 4.5])
        assert result == [2.5, 3.5]

    def test_mixed_int_and_float(self):
        # In Python, 1 == 1.0 is True for set equality, but the value preserved
        # depends on which set contributes it. Here 1 has no match in l2,
        # so only 2.0 and 3.0 appear in the intersection.
        result = common([1, 2, 3], [2.0, 3.0, 4.0])
        assert result == [2.0, 3.0]

    def test_matching_int_and_float(self):
        # When int and float values are numerically equal, they intersect
        result = common([1, 2, 3], [1.0, 2.0, 4.0])
        assert result == [1.0, 2.0]

    def test_boolean_values(self):
        result = common([True, False], [True])
        assert result == [True]


class TestCommonReturnType:
    """Test that return type is correct."""

    def test_returns_list(self):
        result = common([1, 2], [2, 3])
        assert isinstance(result, list)

    def test_returns_unique_elements(self):
        result = common([1, 1, 1], [1, 1, 1])
        assert len(result) == 1

    def test_does_not_modify_original_lists(self):
        l1 = [1, 2, 3]
        l2 = [2, 3, 4]
        l1_copy = l1.copy()
        l2_copy = l2.copy()
        common(l1, l2)
        assert l1 == l1_copy
        assert l2 == l2_copy
