import pytest
from solution import find_Element


class TestFindElement:
    """Tests for the find_Element function."""

    # --- Basic functionality tests ---

    def test_simple_rotation(self):
        """Test a single rotation that shifts an element into view."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 4)]
        rotations = 1
        # Rotation 1: range [0,4]. Index 0 -> becomes 4. So arr[4]=5
        assert find_Element(arr, ranges, rotations, 0) == 5

    def test_index_outside_range_unchanged(self):
        """Test that an index outside all rotation ranges is unchanged."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 2)]
        rotations = 1
        # Index 3 is outside [0,2], so it stays 3. arr[3]=4
        assert find_Element(arr, ranges, rotations, 3) == 4

    def test_no_rotations(self):
        """Test with zero rotations — should return arr[index] directly."""
        arr = [10, 20, 30, 40, 50]
        ranges = []
        rotations = 0
        assert find_Element(arr, ranges, rotations, 2) == 30

    def test_single_element_array(self):
        """Test with a single-element array."""
        arr = [42]
        ranges = [(0, 0)]
        rotations = 1
        assert find_Element(arr, ranges, rotations, 0) == 42

    def test_two_element_array(self):
        """Test with a two-element array."""
        arr = [10, 20]
        ranges = [(0, 1)]
        rotations = 1
        # Index 0 -> right=1, so index becomes 1. arr[1]=20
        assert find_Element(arr, ranges, rotations, 0) == 20
        # Index 1 -> not left, so index becomes 0. arr[0]=10
        assert find_Element(arr, ranges, rotations, 1) == 10

    # --- Multiple rotations ---

    def test_multiple_rotations_applied_in_reverse_order(self):
        """Test that multiple rotations are applied in reverse order."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [(0, 4), (5, 9)]
        rotations = 2
        # Rotations applied in reverse: first (5,9), then (0,4).
        # For index 5: first rotation (5,9): index==left(5) -> index=9.
        #               second rotation (0,4): 9 not in [0,4] -> stays 9.
        # Result: arr[9] = 9
        assert find_Element(arr, ranges, rotations, 5) == 9

    def test_multiple_rotations_complex(self):
        """Test with overlapping rotation ranges."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [(0, 3), (2, 5)]
        rotations = 2
        # Reverse order: first (2,5), then (0,3).
        # For index 2: 
        #   rotation (2,5): index==left(2) -> index=5.
        #   rotation (0,3): 5 not in [0,3] -> stays 5.
        # Result: arr[5] = 5
        assert find_Element(arr, ranges, rotations, 2) == 5

    def test_multiple_rotations_shifted_index(self):
        """Test where index gets shifted by multiple rotations."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [(1, 4), (0, 3)]
        rotations = 2
        # Reverse order: first (0,3), then (1,4).
        # For index 1:
        #   rotation (0,3): 1 != left(0), so index = 1-1 = 0.
        #   rotation (1,4): 0 not in [1,4] -> stays 0.
        # Result: arr[0] = 0
        assert find_Element(arr, ranges, rotations, 1) == 0

    # --- Edge cases ---

    def test_empty_ranges(self):
        """Test with empty ranges list."""
        arr = [1, 2, 3]
        ranges = []
        rotations = 0
        assert find_Element(arr, ranges, rotations, 1) == 2

    def test_zero_rotations_with_nonempty_ranges(self):
        """Test with non-empty ranges but zero rotations."""
        arr = [10, 20, 30, 40]
        ranges = [(0, 3)]
        rotations = 0
        assert find_Element(arr, ranges, rotations, 2) == 30

    def test_index_at_left_boundary(self):
        """Test when index is exactly at the left boundary of a range."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(1, 3)]
        rotations = 1
        # Index 1 == left(1) -> index = right(3). arr[3] = 4
        assert find_Element(arr, ranges, rotations, 1) == 4

    def test_index_at_right_boundary(self):
        """Test when index is exactly at the right boundary of a range."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(1, 3)]
        rotations = 1
        # Index 3 != left(1), so index = 3-1 = 2. arr[2] = 3
        assert find_Element(arr, ranges, rotations, 3) == 3

    def test_index_inside_range_not_at_boundaries(self):
        """Test when index is inside a range but not at boundaries."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(1, 3)]
        rotations = 1
        # Index 2 != left(1), so index = 2-1 = 1. arr[1] = 2
        assert find_Element(arr, ranges, rotations, 2) == 2

    def test_large_array(self):
        """Test with a larger array."""
        arr = list(range(100))
        ranges = [(10, 50)]
        rotations = 1
        # Index 10 == left(10) -> index = 50. arr[50] = 50
        assert find_Element(arr, ranges, rotations, 10) == 50
        # Index 50 != left(10), so index = 49. arr[49] = 49
        assert find_Element(arr, ranges, rotations, 50) == 49
        # Index 30 != left(10), so index = 29. arr[29] = 29
        assert find_Element(arr, ranges, rotations, 30) == 29

    def test_negative_values_in_array(self):
        """Test with negative values in the array."""
        arr = [-5, -3, -1, 0, 2, 4]
        ranges = [(0, 3)]
        rotations = 1
        # Index 0 == left(0) -> index = 3. arr[3] = 0
        assert find_Element(arr, ranges, rotations, 0) == 0

    def test_string_elements(self):
        """Test with string elements in the array."""
        arr = ["a", "b", "c", "d", "e"]
        ranges = [(0, 4)]
        rotations = 1
        # Index 0 == left(0) -> index = 4. arr[4] = "e"
        assert find_Element(arr, ranges, rotations, 0) == "e"

    def test_float_elements(self):
        """Test with float elements in the array."""
        arr = [1.1, 2.2, 3.3, 4.4, 5.5]
        ranges = [(0, 2)]
        rotations = 1
        # Index 0 == left(0) -> index = 2. arr[2] = 3.3
        assert find_Element(arr, ranges, rotations, 0) == 3.3

    # --- Parameter validation / boundary conditions ---

    def test_single_range(self):
        """Test with a single range entry."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 4)]
        rotations = 1
        assert find_Element(arr, ranges, rotations, 2) == 1

    def test_overlapping_ranges(self):
        """Test with overlapping rotation ranges."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [(0, 5), (3, 8)]
        rotations = 2
        # Reverse order: first (3,8), then (0,5).
        # For index 3:
        #   rotation (3,8): index==left(3) -> index=8.
        #   rotation (0,5): 8 not in [0,5] -> stays 8.
        # Result: arr[8] = 8
        assert find_Element(arr, ranges, rotations, 3) == 8

    def test_disjoint_ranges(self):
        """Test with disjoint (non-overlapping) rotation ranges."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [(0, 2), (7, 9)]
        rotations = 2
        # Reverse order: first (7,9), then (0,2).
        # For index 7:
        #   rotation (7,9): index==left(7) -> index=9.
        #   rotation (0,2): 9 not in [0,2] -> stays 9.
        # Result: arr[9] = 9
        assert find_Element(arr, ranges, rotations, 7) == 9

    def test_index_exactly_one_past_right_boundary(self):
        """Test index just past the right boundary of a range."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 3)]
        rotations = 1
        # Index 4 is outside [0,3], so unchanged. arr[4] = 5
        assert find_Element(arr, ranges, rotations, 4) == 5

    def test_index_exactly_one_before_left_boundary(self):
        """Test index just before the left boundary of a range."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(2, 4)]
        rotations = 1
        # Index 1 is outside [2,4], so unchanged. arr[1] = 2
        assert find_Element(arr, ranges, rotations, 1) == 2

    def test_many_rotations_same_range(self):
        """Test many rotations all using the same range."""
        arr = [0, 1, 2, 3, 4]
        ranges = [(0, 4), (0, 4), (0, 4)]
        rotations = 3
        # Reverse order: three times apply (0,4).
        # For index 0:
        #   rot1 (0,4): index==0 -> index=4.
        #   rot2 (0,4): index=4, left=0, right=4. 4!=0, so index=4-1=3.
        #   rot3 (0,4): index=3, left=0, right=4. 3!=0, so index=3-1=2.
        # Result: arr[2] = 2
        assert find_Element(arr, ranges, rotations, 0) == 2

    def test_rotations_greater_than_ranges_length(self):
        """Test when rotations count exceeds the number of ranges provided."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 2)]
        rotations = 3
        # The loop runs from rotations-1 down to 0, accessing ranges[i].
        # This would cause an IndexError if i >= len(ranges).
        # Based on the implementation, this is expected behavior (IndexError).
        with pytest.raises(IndexError):
            find_Element(arr, ranges, rotations, 0)

    def test_equal_left_and_right(self):
        """Test with a range where left equals right."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(2, 2)]
        rotations = 1
        # Index 2 == left(2) -> index = right(2). Stays 2. arr[2] = 3
        assert find_Element(arr, ranges, rotations, 2) == 3
        # Index 1 is outside [2,2], unchanged. arr[1] = 2
        assert find_Element(arr, ranges, rotations, 1) == 2

    def test_all_indices_covered_by_range(self):
        """Test that all indices in a full-range rotation behave correctly."""
        arr = [0, 1, 2, 3, 4]
        ranges = [(0, 4)]
        rotations = 1
        results = [find_Element(arr, ranges, rotations, i) for i in range(5)]
        # Index 0 -> 4, 1 -> 0, 2 -> 1, 3 -> 2, 4 -> 3
        assert results == [4, 0, 1, 2, 3]
