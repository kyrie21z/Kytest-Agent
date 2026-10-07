import pytest
from solution import find_Element


class TestFindElement:
    """Tests for the find_Element function."""

    # --- Basic functionality: no rotations ---

    def test_no_rotations_returns_original(self):
        """With zero rotations, the element at any valid index is unchanged."""
        arr = [10, 20, 30, 40, 50]
        assert find_Element(arr, [], 0, 0) == 10
        assert find_Element(arr, [], 0, 2) == 30
        assert find_Element(arr, [], 0, 4) == 50

    def test_single_element_no_rotations(self):
        """Single-element array with no rotations returns that element."""
        arr = [42]
        assert find_Element(arr, [], 0, 0) == 42

    # --- Single rotation ---

    def test_single_rotation_left_shift(self):
        """A single rotation shifts elements left within the given range."""
        # Range [1, 4] means indices 1-4 are rotated left by 1.
        # Original: [10, 20, 30, 40, 50]
        # After rotating [1..4] left by 1: [10, 30, 40, 50, 20]
        arr = [10, 20, 30, 40, 50]
        ranges = [(1, 4)]
        assert find_Element(arr, ranges, 1, 0) == 10   # index 0 unchanged
        assert find_Element(arr, ranges, 1, 1) == 30   # was at index 2
        assert find_Element(arr, ranges, 1, 2) == 40   # was at index 3
        assert find_Element(arr, ranges, 1, 3) == 50   # was at index 4
        assert find_Element(arr, ranges, 1, 4) == 20   # was at index 1

    def test_single_rotation_wraps_around(self):
        """The leftmost element in the range wraps to the rightmost position."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 3)]
        # Rotating [0..3] left by 1: [4, 1, 2, 3, 5]
        assert find_Element(arr, ranges, 1, 0) == 4
        assert find_Element(arr, ranges, 1, 1) == 1
        assert find_Element(arr, ranges, 1, 2) == 2
        assert find_Element(arr, ranges, 1, 3) == 3
        assert find_Element(arr, ranges, 1, 4) == 5

    def test_single_rotation_full_range(self):
        """Rotation covers the entire array."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 4)]
        # Rotating [0..4] left by 1: [2, 3, 4, 5, 1]
        assert find_Element(arr, ranges, 1, 0) == 2
        assert find_Element(arr, ranges, 1, 1) == 3
        assert find_Element(arr, ranges, 1, 2) == 4
        assert find_Element(arr, ranges, 1, 3) == 5
        assert find_Element(arr, ranges, 1, 4) == 1

    # --- Multiple rotations ---

    def test_multiple_rotations_applied_in_reverse(self):
        """Multiple rotations are applied in reverse order."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 2), (1, 4)]
        # Rotation 1 (index 0): rotate [0..2] left -> [2, 3, 1, 4, 5]
        # Rotation 2 (index 1): rotate [1..4] left -> [2, 3, 4, 5, 1]
        # But we trace backwards: start from final index and apply rot 1 then rot 0.
        # For index 0: never in any range -> stays 0 -> arr[0]=2
        # For index 1: in rot 1 ([1..4]) -> index becomes 0; not in rot 0 ([0..2]) but index=0 so index=2; arr[2]=1
        assert find_Element(arr, ranges, 2, 0) == 2
        assert find_Element(arr, ranges, 2, 1) == 1
        assert find_Element(arr, ranges, 2, 2) == 3
        assert find_Element(arr, ranges, 2, 3) == 4
        assert find_Element(arr, ranges, 2, 4) == 5

    def test_overlapping_ranges(self):
        """Overlapping rotation ranges are handled correctly."""
        arr = [1, 2, 3, 4, 5, 6]
        ranges = [(0, 3), (2, 5)]
        # Apply rot 1 first: rotate [2..5] left -> [1, 2, 4, 5, 6, 3]
        # Then apply rot 0: rotate [0..3] left -> [2, 4, 5, 1, 6, 3]
        assert find_Element(arr, ranges, 2, 0) == 2
        assert find_Element(arr, ranges, 2, 1) == 4
        assert find_Element(arr, ranges, 2, 2) == 5
        assert find_Element(arr, ranges, 2, 3) == 1
        assert find_Element(arr, ranges, 2, 4) == 6
        assert find_Element(arr, ranges, 2, 5) == 3

    def test_non_overlapping_ranges(self):
        """Non-overlapping rotation ranges work independently."""
        arr = [1, 2, 3, 4, 5, 6, 7]
        ranges = [(0, 2), (4, 6)]
        # Rot 1: rotate [4..6] left -> [1, 2, 3, 4, 6, 7, 5]
        # Rot 0: rotate [0..2] left -> [2, 3, 1, 4, 6, 7, 5]
        assert find_Element(arr, ranges, 2, 0) == 2
        assert find_Element(arr, ranges, 2, 1) == 3
        assert find_Element(arr, ranges, 2, 2) == 1
        assert find_Element(arr, ranges, 2, 3) == 4
        assert find_Element(arr, ranges, 2, 4) == 6
        assert find_Element(arr, ranges, 2, 5) == 7
        assert find_Element(arr, ranges, 2, 6) == 5

    # --- Edge cases ---

    def test_empty_array(self):
        """Empty array should raise IndexError or return nothing meaningful."""
        arr = []
        with pytest.raises(IndexError):
            find_Element(arr, [], 0, 0)

    def test_index_out_of_bounds_raises_error(self):
        """Accessing an index beyond the array length raises IndexError."""
        arr = [1, 2, 3]
        with pytest.raises(IndexError):
            find_Element(arr, [], 0, 3)
        with pytest.raises(IndexError):
            find_Element(arr, [], 0, 100)

    def test_negative_index(self):
        """Negative indices are valid Python indices and should work."""
        arr = [10, 20, 30, 40, 50]
        assert find_Element(arr, [], 0, -1) == 50
        assert find_Element(arr, [], 0, -3) == 30

    def test_single_element_with_rotation(self):
        """Single element array with rotation still returns that element."""
        arr = [99]
        ranges = [(0, 0)]
        assert find_Element(arr, ranges, 1, 0) == 99

    def test_rotation_range_is_single_element(self):
        """A rotation range covering only one element has no effect."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(2, 2)]
        assert find_Element(arr, ranges, 1, 0) == 1
        assert find_Element(arr, ranges, 1, 1) == 2
        assert find_Element(arr, ranges, 1, 2) == 3
        assert find_Element(arr, ranges, 1, 3) == 4
        assert find_Element(arr, ranges, 1, 4) == 5

    def test_index_not_in_any_rotation_range(self):
        """Indices outside all rotation ranges remain unchanged."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(1, 3)]
        assert find_Element(arr, ranges, 1, 0) == 1
        assert find_Element(arr, ranges, 1, 4) == 5

    def test_large_array(self):
        """Works correctly with a larger array."""
        arr = list(range(100))
        ranges = [(10, 50)]
        result = find_Element(arr, ranges, 1, 10)
        assert result == 11
        result = find_Element(arr, ranges, 1, 50)
        assert result == 10

    def test_zero_rotations_with_ranges_provided(self):
        """Zero rotations means ranges are ignored entirely."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 4), (1, 3)]
        assert find_Element(arr, ranges, 0, 0) == 1
        assert find_Element(arr, ranges, 0, 2) == 3
        assert find_Element(arr, ranges, 0, 4) == 5

    def test_multiple_same_range_rotations(self):
        """Applying the same range multiple times rotates cumulatively."""
        arr = [1, 2, 3, 4, 5]
        ranges = [(0, 4), (0, 4)]
        # First rotation (applied last): [2, 3, 4, 5, 1]
        # Second rotation (applied first): [3, 4, 5, 1, 2]
        assert find_Element(arr, ranges, 2, 0) == 3
        assert find_Element(arr, ranges, 2, 1) == 4
        assert find_Element(arr, ranges, 2, 2) == 5
        assert find_Element(arr, ranges, 2, 3) == 1
        assert find_Element(arr, ranges, 2, 4) == 2

    def test_string_array(self):
        """Function works with arrays of strings."""
        arr = ['a', 'b', 'c', 'd', 'e']
        ranges = [(0, 3)]
        assert find_Element(arr, ranges, 1, 0) == 'd'
        assert find_Element(arr, ranges, 1, 1) == 'a'
        assert find_Element(arr, ranges, 1, 2) == 'b'
        assert find_Element(arr, ranges, 1, 3) == 'c'
        assert find_Element(arr, ranges, 1, 4) == 'e'

    def test_float_array(self):
        """Function works with arrays of floats."""
        arr = [1.1, 2.2, 3.3, 4.4, 5.5]
        ranges = [(1, 3)]
        assert find_Element(arr, ranges, 1, 0) == 1.1
        assert find_Element(arr, ranges, 1, 1) == 3.3
        assert find_Element(arr, ranges, 1, 2) == 4.4
        assert find_Element(arr, ranges, 1, 3) == 2.2
        assert find_Element(arr, ranges, 1, 4) == 5.5

    def test_mixed_type_array(self):
        """Function works with arrays containing mixed types."""
        arr = [1, 'hello', 3.14, None, True]
        ranges = [(0, 4)]
        assert find_Element(arr, ranges, 1, 0) == 'hello'
        assert find_Element(arr, ranges, 1, 1) == 3.14
        assert find_Element(arr, ranges, 1, 2) == None
        assert find_Element(arr, ranges, 1, 3) == True
        assert find_Element(arr, ranges, 1, 4) == 1

    def test_boundary_index_at_left_edge(self):
        """Index exactly at the left edge of a rotation range wraps to right."""
        arr = [10, 20, 30, 40, 50]
        ranges = [(1, 4)]
        assert find_Element(arr, ranges, 1, 1) == 30  # left edge -> next element

    def test_boundary_index_at_right_edge(self):
        """Index exactly at the right edge of a rotation range gets the leftmost value."""
        arr = [10, 20, 30, 40, 50]
        ranges = [(1, 4)]
        assert find_Element(arr, ranges, 1, 4) == 20  # right edge -> leftmost of range

    def test_many_rotations_on_small_array(self):
        """Many rotations on a small array still produces correct results."""
        arr = [1, 2, 3]
        ranges = [(0, 2), (0, 2), (0, 2)]
        # Each rotation shifts left by 1. Three rotations shift left by 3 = full cycle.
        # So the array should be back to original.
        assert find_Element(arr, ranges, 3, 0) == 1
        assert find_Element(arr, ranges, 3, 1) == 2
        assert find_Element(arr, ranges, 3, 2) == 3
