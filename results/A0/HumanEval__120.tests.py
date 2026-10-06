import pytest
from solution import maximum


class TestMaximumBasic:
    """Test basic functionality with examples from the docstring."""

    def test_example_1(self):
        """Example 1: all elements, negative numbers included."""
        assert maximum([-3, -4, 5], 3) == [-4, -3, 5]

    def test_example_2(self):
        """Example 2: duplicates, partial selection."""
        assert maximum([4, -4, 4], 2) == [4, 4]

    def test_example_3(self):
        """Example 3: single element result."""
        assert maximum([-3, 2, 1, 2, -1, -2, 1], 1) == [2]


class TestMaximumEdgeCases:
    """Test edge cases."""

    def test_k_equals_zero(self):
        """When k is 0, return empty list."""
        assert maximum([1, 2, 3], 0) == []

    def test_k_equals_array_length(self):
        """When k equals array length, return sorted array."""
        assert maximum([3, 1, 2], 3) == [1, 2, 3]

    def test_single_element_array(self):
        """Single element array."""
        assert maximum([42], 1) == [42]

    def test_single_element_array_k_zero(self):
        """Single element array with k=0."""
        assert maximum([42], 0) == []

    def test_two_elements(self):
        """Two element array."""
        assert maximum([5, 10], 1) == [10]
        assert maximum([5, 10], 2) == [5, 10]


class TestMaximumWithNegatives:
    """Test with negative numbers."""

    def test_all_negative(self):
        """All negative numbers."""
        assert maximum([-5, -1, -3], 2) == [-3, -1]

    def test_mixed_positive_negative(self):
        """Mix of positive and negative numbers."""
        assert maximum([-10, 0, 10], 2) == [0, 10]

    def test_larger_negative_selection(self):
        """Selecting largest (least negative) values."""
        assert maximum([-100, -50, -75, -25], 3) == [-75, -50, -25]


class TestMaximumWithDuplicates:
    """Test with duplicate values."""

    def test_all_same_values(self):
        """All elements are the same."""
        assert maximum([7, 7, 7, 7], 3) == [7, 7, 7]

    def test_partial_duplicates(self):
        """Some duplicates in the array."""
        assert maximum([1, 2, 2, 3, 3, 3], 4) == [2, 3, 3, 3]

    def test_duplicate_max_values(self):
        """Multiple copies of the max value selected."""
        assert maximum([5, 5, 5, 1, 2], 3) == [5, 5, 5]


class TestMaximumSortedInput:
    """Test with already sorted inputs."""

    def test_already_sorted_ascending(self):
        """Input already sorted ascending."""
        assert maximum([1, 2, 3, 4, 5], 3) == [3, 4, 5]

    def test_already_sorted_descending(self):
        """Input already sorted descending."""
        assert maximum([5, 4, 3, 2, 1], 3) == [3, 4, 5]

    def test_reverse_sorted_partial(self):
        """Reverse sorted, select middle portion."""
        assert maximum([10, 8, 6, 4, 2], 2) == [8, 10]


class TestMaximumLargeValues:
    """Test with large values within the specified range."""

    def test_boundary_values(self):
        """Test with boundary values [-1000, 1000]."""
        assert maximum([-1000, 1000, 0], 2) == [0, 1000]

    def test_all_zeros(self):
        """All zeros."""
        assert maximum([0, 0, 0, 0], 3) == [0, 0, 0]

    def test_large_range(self):
        """Wide range of values."""
        arr = list(range(-100, 100))
        result = maximum(arr, 5)
        assert result == [95, 96, 97, 98, 99]


class TestMaximumReturnProperties:
    """Test that the return value satisfies expected properties."""

    def test_result_length_equals_k(self):
        """Result length should always equal k."""
        for k in range(6):
            result = maximum([1, 2, 3, 4, 5], k)
            assert len(result) == k

    def test_result_is_sorted(self):
        """Result should be sorted in ascending order."""
        result = maximum([5, 3, 1, 4, 2], 4)
        assert result == sorted(result)

    def test_result_contains_only_original_elements(self):
        """All elements in result must come from original array."""
        arr = [10, -5, 20, 0, 15]
        result = maximum(arr, 3)
        for elem in result:
            assert elem in arr

    def test_result_has_correct_count_of_each_value(self):
        """Each value in result appears at most as many times as in input."""
        arr = [1, 1, 1, 2, 2, 3]
        result = maximum(arr, 4)
        for val in set(result):
            assert result.count(val) <= arr.count(val)

    def test_result_contains_top_k_largest(self):
        """Result contains exactly the k largest elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        top_k = sorted(arr, reverse=True)[:3]
        result = maximum(arr, 3)
        assert sorted(result) == sorted(top_k)
