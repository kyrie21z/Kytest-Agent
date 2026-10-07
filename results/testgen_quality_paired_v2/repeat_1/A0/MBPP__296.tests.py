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
        """A sorted two-element array has zero inversions."""
        assert get_Inv_Count([1, 2]) == 0

    def test_two_elements_unsorted(self):
        """An unsorted two-element array has one inversion."""
        assert get_Inv_Count([2, 1]) == 1

    def test_already_sorted(self):
        """A fully sorted array has zero inversions."""
        assert get_Inv_Count([1, 2, 3, 4, 5]) == 0

    def test_reverse_sorted(self):
        """A reverse-sorted array has n*(n-1)/2 inversions."""
        # [5, 4, 3, 2, 1] -> 4+3+2+1 = 10 inversions
        assert get_Inv_Count([5, 4, 3, 2, 1]) == 10

    def test_all_same_elements(self):
        """An array with all identical elements has zero inversions."""
        assert get_Inv_Count([3, 3, 3, 3]) == 0

    def test_negative_numbers(self):
        """Function should handle negative numbers correctly."""
        # [-1, -3, 2, 0] -> (-1 > -3), (2 > 0), (2 > -3 no, wait...)
        # Pairs: (-1,-3): -1 > -3 yes; (-1,2): no; (-1,0): no
        #         (-3,2): no; (-3,0): no; (2,0): yes
        # Total = 2
        assert get_Inv_Count([-1, -3, 2, 0]) == 2

    def test_mixed_positive_and_negative(self):
        """Function should handle mixed positive and negative numbers."""
        # [3, -2, 1] -> (3 > -2), (3 > 1), (-2 > 1 no)
        # Total = 2
        assert get_Inv_Count([3, -2, 1]) == 2

    def test_duplicates(self):
        """Function should handle duplicate values correctly."""
        # [2, 2, 1] -> (2 > 2 no), (2 > 1 yes), (2 > 1 yes)
        # Total = 2
        assert get_Inv_Count([2, 2, 1]) == 2

    def test_larger_sorted_array(self):
        """Test with a larger sorted array."""
        assert get_Inv_Count(list(range(1, 101))) == 0

    def test_larger_reverse_sorted_array(self):
        """Test with a larger reverse-sorted array."""
        arr = list(range(10, 0, -1))  # [10, 9, ..., 1]
        # Expected inversions: 9+8+7+6+5+4+3+2+1 = 45
        assert get_Inv_Count(arr) == 45

    def test_complex_case(self):
        """Test with a more complex array."""
        # [7, 5, 6, 4]
        # Pairs: (7,5) yes, (7,6) yes, (7,4) yes
        #        (5,6) no, (5,4) yes
        #        (6,4) yes
        # Total = 5
        assert get_Inv_Count([7, 5, 6, 4]) == 5

    def test_returns_integer(self):
        """Ensure the return type is an integer."""
        result = get_Inv_Count([3, 1, 2])
        assert isinstance(result, int)

    def test_zero_inversions_simple(self):
        """Verify zero inversions for simple sorted input."""
        assert get_Inv_Count([1, 2, 3]) == 0

    def test_one_inversion_simple(self):
        """Verify one inversion for minimal unsorted input."""
        assert get_Inv_Count([2, 1, 3]) == 1
