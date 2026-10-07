import pytest
from solution import find_Element


class TestFindElementBasic:
    """Test basic functionality of find_Element."""

    def test_no_rotations(self):
        """When rotations is 0, the element at the given index should be returned unchanged."""
        arr = [10, 20, 30, 40, 50]
        ranges = []
        result = find_Element(arr, ranges, 0, 2)
        assert result == 30

    def test_single_element_array(self):
        """Array with one element should always return that element."""
        arr = [42]
        ranges = []
        result = find_Element(arr, ranges, 0, 0)
        assert result == 42

    def test_index_zero(self):
        """Accessing index 0 without any effective rotation."""
        arr = [1, 2, 3, 4, 5]
        ranges = []
        result = find_Element(arr, ranges, 0, 0)
        assert result == 1

    def test_index_last(self):
        """Accessing the last index without any effective rotation."""
        arr = [1, 2, 3, 4, 5]
        ranges = []
        result = find_Element(arr, ranges, 0, 4)
        assert result == 5

    def test_simple_rotation_shifts_index(self):
        """A single rotation range should shift the index accordingly."""
        # Range [1, 3]: indices 1->1(right), 2->1, 3->1
        # So index 2 maps to index 1 after this rotation
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 1, 2)
        assert result == 20

    def test_rotation_wraps_left_to_right(self):
        """When index equals left boundary, it wraps to right boundary."""
        # Range [1, 3]: index 1 -> 3
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 1, 1)
        assert result == 40

    def test_rotation_inside_range(self):
        """Index inside the range (not at boundaries) shifts left by 1."""
        # Range [1, 3]: index 2 -> 1
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 1, 2)
        assert result == 20

    def test_rotation_index_at_right_boundary(self):
        """Index at right boundary shifts left by 1."""
        # Range [1, 3]: index 3 -> 2
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 1, 3)
        assert result == 30


class TestFindElementMultipleRotations:
    """Test behavior with multiple rotation ranges."""

    def test_multiple_rotations_applied_in_reverse(self):
        """Rotations are applied in reverse order (last rotation first)."""
        # Two rotations: [1,3] then [0,2]
        # Applied in reverse: first [0,2], then [1,3]
        # Start with index 0:
        #   After [0,2]: index 0 -> 2 (left boundary wraps to right)
        #   After [1,3]: index 2 is in [1,3], so 2 -> 1
        # Final index = 1, arr[1] = 20
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3], [0, 2]]
        result = find_Element(arr, ranges, 2, 0)
        assert result == 20

    def test_multiple_rotations_no_effect_on_index(self):
        """If index doesn't fall in any rotation range, it stays the same."""
        arr = [10, 20, 30, 40, 50]
        ranges = [[0, 1], [3, 4]]
        result = find_Element(arr, ranges, 2, 2)
        assert result == 30

    def test_overlapping_ranges(self):
        """Overlapping ranges should still work correctly with reverse application."""
        # Ranges: [1,4], [2,3]
        # Reverse: apply [2,3] first, then [1,4]
        # Index 2: [2,3] -> 2 is left boundary -> 3; then [1,4] -> 3 is inside -> 2
        # Final index = 2, arr[2] = 30
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 4], [2, 3]]
        result = find_Element(arr, ranges, 2, 2)
        assert result == 30

    def test_three_rotations(self):
        """Three consecutive rotations applied in reverse."""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ranges = [[0, 4], [2, 6], [1, 3]]
        # Reverse order: [1,3], [2,6], [0,4]
        # Index 1: [1,3] -> 1 is left -> 3; [2,6] -> 3 is inside -> 2; [0,4] -> 2 is inside -> 1
        # Final index = 1, arr[1] = 2
        result = find_Element(arr, ranges, 3, 1)
        assert result == 2


class TestFindElementEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_ranges_list(self):
        """Empty ranges list means no rotations."""
        arr = [5, 10, 15, 20]
        result = find_Element(arr, [], 0, 1)
        assert result == 10

    def test_single_element_range(self):
        """Range where left == right (single element range)."""
        # Range [2, 2]: index 2 is left boundary -> wraps to 2 (same)
        arr = [10, 20, 30, 40, 50]
        ranges = [[2, 2]]
        result = find_Element(arr, ranges, 1, 2)
        assert result == 30

    def test_full_array_rotation(self):
        """Rotation covers the entire array."""
        # Range [0, 4]: every index is affected
        # Index 0 -> 4, 1 -> 0, 2 -> 1, 3 -> 2, 4 -> 3
        arr = [10, 20, 30, 40, 50]
        ranges = [[0, 4]]
        result = find_Element(arr, ranges, 1, 0)
        assert result == 50

    def test_large_array(self):
        """Works correctly with larger arrays."""
        arr = list(range(100))
        ranges = [[10, 50]]
        # Index 10 is left boundary -> wraps to 50
        result = find_Element(arr, ranges, 1, 10)
        assert result == 50

    def test_negative_scenario_index_outside_all_ranges(self):
        """Index outside all rotation ranges remains unchanged."""
        arr = [100, 200, 300, 400, 500]
        ranges = [[0, 1], [3, 4]]
        result = find_Element(arr, ranges, 2, 2)
        assert result == 300

    def test_string_elements(self):
        """Function works with non-numeric elements."""
        arr = ['a', 'b', 'c', 'd', 'e']
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 1, 1)
        assert result == 'd'

    def test_float_elements(self):
        """Function works with float elements."""
        arr = [1.1, 2.2, 3.3, 4.4, 5.5]
        ranges = [[0, 2]]
        result = find_Element(arr, ranges, 1, 0)
        assert result == 3.3

    def test_mixed_type_elements(self):
        """Function works with mixed type elements."""
        arr = [1, 'two', 3.0, None, True]
        ranges = [[0, 4]]
        result = find_Element(arr, ranges, 1, 0)
        assert result == True


class TestFindElementValidation:
    """Test input validation and error handling."""

    def test_index_out_of_bounds_raises_error(self):
        """Accessing an index beyond array bounds should raise IndexError."""
        arr = [1, 2, 3]
        ranges = []
        with pytest.raises(IndexError):
            find_Element(arr, ranges, 0, 3)

    def test_negative_index_works(self):
        """Negative index works via Python's native negative indexing."""
        arr = [1, 2, 3, 4, 5]
        ranges = []
        result = find_Element(arr, ranges, 0, -1)
        assert result == 5  # arr[-1] = 5

    def test_invalid_range_left_greater_than_right(self):
        """Range with left > right: index won't match since condition is left <= index <= right."""
        arr = [10, 20, 30, 40, 50]
        ranges = [[3, 1]]  # Invalid range, no index will satisfy left <= index <= right
        result = find_Element(arr, ranges, 1, 2)
        assert result == 30  # No rotation effect, original index 2

    def test_empty_array_raises_error(self):
        """Empty array should raise IndexError for any index access."""
        arr = []
        ranges = []
        with pytest.raises(IndexError):
            find_Element(arr, ranges, 0, 0)

    def test_zero_rotations_with_nonempty_ranges(self):
        """Zero rotations means no rotation logic is applied regardless of ranges."""
        arr = [10, 20, 30, 40, 50]
        ranges = [[1, 3]]
        result = find_Element(arr, ranges, 0, 2)
        assert result == 30


class TestFindElementComprehensive:
    """Comprehensive integration-style tests."""

    def test_complex_multi_rotation_scenario(self):
        """Complex scenario with multiple overlapping rotations."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ranges = [[0, 5], [3, 8], [1, 6]]
        # Reverse: [1,6], [3,8], [0,5]
        # Index 1: [1,6] -> left boundary -> 6; [3,8] -> inside -> 5; [0,5] -> right boundary -> 4
        # Final index = 4, arr[4] = 4
        result = find_Element(arr, ranges, 3, 1)
        assert result == 4

    def test_identity_rotation(self):
        """A rotation that maps index back to itself."""
        arr = [10, 20, 30, 40, 50]
        ranges = [[2, 2]]  # Single element range, index stays the same
        result = find_Element(arr, ranges, 1, 2)
        assert result == 30

    def test_cascading_rotation_effects(self):
        """Each rotation can affect the index set by previous (reverse-order) rotations."""
        arr = [100, 200, 300, 400, 500, 600, 700]
        ranges = [[0, 3], [2, 5]]
        # Reverse: [2,5], [0,3]
        # Index 2: [2,5] -> left boundary -> 5; [0,3] -> not in range -> stays 5
        # Final index = 5, arr[5] = 600
        result = find_Element(arr, ranges, 2, 2)
        assert result == 600

    def test_deterministic_result(self):
        """Same inputs should always produce the same output."""
        arr = [5, 10, 15, 20, 25, 30]
        ranges = [[1, 4], [0, 2], [3, 5]]
        expected = find_Element(arr, ranges, 3, 3)
        for _ in range(10):
            assert find_Element(arr, ranges, 3, 3) == expected
