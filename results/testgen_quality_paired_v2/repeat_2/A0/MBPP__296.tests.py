import pytest
from solution import get_Inv_Count


class TestGetInvCount:
    """Unit tests for the get_Inv_Count function."""

    def test_empty_array(self):
        """An empty array has zero inversions."""
        assert get_Inv_Count([]) == 0

    def test_single_element(self):
        """A single-element array has zero inversions."""
        assert get_Inv_Count([1]) == 0

    def test_two_elements_sorted(self):
        """Two elements in ascending order have zero inversions."""
        assert get_Inv_Count([1, 2]) == 0

    def test_two_elements_reversed(self):
        """Two elements in descending order have one inversion."""
        assert get_Inv_Count([2, 1]) == 1

    def test_already_sorted(self):
        """A fully sorted array has zero inversions."""
        assert get_Inv_Count([1, 2, 3, 4, 5]) == 0

    def test_reverse_sorted(self):
        """A fully reverse-sorted array has n*(n-1)/2 inversions."""
        # [5, 4, 3, 2, 1] -> 4+3+2+1 = 10 inversions
        assert get_Inv_Count([5, 4, 3, 2, 1]) == 10

    def test_reverse_sorted_n3(self):
        """Reverse sorted array of length 3 has 3 inversions."""
        # [3, 2, 1] -> 2+1 = 3 inversions
        assert get_Inv_Count([3, 2, 1]) == 3

    def test_reverse_sorted_n4(self):
        """Reverse sorted array of length 4 has 6 inversions."""
        # [4, 3, 2, 1] -> 3+2+1 = 6 inversions
        assert get_Inv_Count([4, 3, 2, 1]) == 6

    def test_all_same_elements(self):
        """An array with all identical elements has zero inversions."""
        assert get_Inv_Count([3, 3, 3, 3]) == 0

    def test_duplicates_with_inversions(self):
        """Array with duplicates and some inversions."""
        # [2, 1, 2, 1] -> pairs: (2,1)@0,1; (2,1)@0,3; (2,1)@2,3 => 3 inversions
        assert get_Inv_Count([2, 1, 2, 1]) == 3

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # [-1, -3, -2] -> (-1 > -3), (-1 > -2) => 2 inversions
        assert get_Inv_Count([-1, -3, -2]) == 2

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
        # [3, -1, 2] -> (3 > -1), (3 > 2) => 2 inversions
        assert get_Inv_Count([3, -1, 2]) == 2

    def test_large_inversion_count(self):
        """Test with a larger array having many inversions."""
        # [5, 3, 1, 4, 2]
        # Pairs: (5,3),(5,1),(5,4),(5,2),(3,1),(3,2),(1,none),(4,2)
        # = 4 + 2 + 0 + 1 + 0 = 7 inversions
        assert get_Inv_Count([5, 3, 1, 4, 2]) == 7

    def test_one_inversion(self):
        """Array with exactly one inversion."""
        assert get_Inv_Count([1, 3, 2, 4, 5]) == 1

    def test_many_inversions(self):
        """Array with multiple scattered inversions."""
        # [4, 1, 3, 2]
        # (4,1),(4,3),(4,2),(1,none),(3,2) = 4 inversions
        assert get_Inv_Count([4, 1, 3, 2]) == 4

    def test_larger_sorted_array(self):
        """Verify zero inversions for a longer sorted array."""
        assert get_Inv_Count(list(range(1, 101))) == 0

    def test_larger_reverse_sorted_array(self):
        """Verify max inversions for a longer reverse sorted array."""
        arr = list(range(10, 0, -1))  # [10, 9, ..., 1]
        expected = 10 * 9 // 2  # 45
        assert get_Inv_Count(arr) == expected

    def test_random_like_array(self):
        """Test with a moderately shuffled array."""
        # [1, 5, 4, 3, 2]
        # (1,none),(5,4),(5,3),(5,2),(4,3),(4,2),(3,2) = 6 inversions
        assert get_Inv_Count([1, 5, 4, 3, 2]) == 6
