import pytest
from solution import get_Inv_Count


class TestGetInvCount:
    """Tests for the get_Inv_Count function."""

    def test_empty_array(self):
        """An empty array has zero inversions."""
        assert get_Inv_Count([]) == 0

    def test_single_element(self):
        """A single-element array has zero inversions."""
        assert get_Inv_Count([1]) == 0

    def test_two_elements_sorted(self):
        """A sorted two-element array has zero inversions."""
        assert get_Inv_Count([1, 2]) == 0

    def test_two_elements_unsorted(self):
        """An unsorted two-element array has one inversion."""
        assert get_Inv_Count([2, 1]) == 1

    def test_already_sorted(self):
        """A fully sorted array has zero inversions."""
        assert get_Inv_Count([1, 2, 3, 4, 5]) == 0

    def test_reverse_sorted(self):
        """A reverse-sorted array of n elements has n*(n-1)/2 inversions."""
        # [5, 4, 3, 2, 1] -> 4+3+2+1 = 10 inversions
        assert get_Inv_Count([5, 4, 3, 2, 1]) == 10

    def test_reverse_sorted_three(self):
        # [3, 2, 1] -> 2+1 = 3 inversions
        assert get_Inv_Count([3, 2, 1]) == 3

    def test_no_inversions(self):
        """Array with no inversions."""
        assert get_Inv_Count([1, 3, 5, 7, 9]) == 0

    def test_some_inversions(self):
        """Array with some inversions."""
        # [1, 3, 2, 5, 4] -> (3,2), (5,4) = 2 inversions
        assert get_Inv_Count([1, 3, 2, 5, 4]) == 2

    def test_all_same_elements(self):
        """An array with all identical elements has zero inversions."""
        assert get_Inv_Count([3, 3, 3, 3]) == 0

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # [-1, -3, 2, 0] -> (-1,-3), (-3,2) no wait...
        # Pairs: (-1,-3): -1 > -3 => yes; (-1,2): no; (-1,0): no
        #         (-3,2): no; (-3,0): no; (2,0): 2 > 0 => yes
        # Total: 2 inversions
        assert get_Inv_Count([-1, -3, 2, 0]) == 2

    def test_mixed_positive_and_negative(self):
        """Test with mixed positive and negative numbers."""
        # [3, -2, 5, -1, 4]
        # (3,-2): yes; (3,5): no; (3,-1): yes; (3,4): no
        # (-2,5): no; (-2,-1): no; (-2,4): no
        # (5,-1): yes; (5,4): yes
        # (-1,4): no
        # Total: 4 inversions
        assert get_Inv_Count([3, -2, 5, -1, 4]) == 4

    def test_larger_array(self):
        """Test with a larger array."""
        # [8, 4, 2, 1] -> (8,4),(8,2),(8,1),(4,2),(4,1),(2,1) = 6
        assert get_Inv_Count([8, 4, 2, 1]) == 6

    def test_duplicate_values_with_inversions(self):
        """Test with duplicate values where inversions still exist."""
        # [2, 2, 1] -> (2,1) at index 0, (2,1) at index 1 = 2
        assert get_Inv_Count([2, 2, 1]) == 2

    def test_large_inversion_count(self):
        """Test with a larger reverse-sorted array."""
        # [5, 4, 3, 2, 1, 0] -> 5+4+3+2+1 = 15
        assert get_Inv_Count([5, 4, 3, 2, 1, 0]) == 15
