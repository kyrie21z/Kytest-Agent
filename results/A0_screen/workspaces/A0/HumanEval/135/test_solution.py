import pytest
from solution import can_arrange


class TestCanArrange:
    """Tests for the can_arrange function."""

    def test_basic_violation(self):
        """Example from docstring: violation at index 3."""
        assert can_arrange([1, 2, 4, 3, 5]) == 3

    def test_no_violation_increasing(self):
        """Strictly increasing array has no violation."""
        assert can_arrange([1, 2, 3]) == -1

    def test_no_violation_single_element(self):
        """Single-element array has no preceding element."""
        assert can_arrange([42]) == -1

    def test_no_violation_empty_array(self):
        """Empty array has no elements to compare."""
        assert can_arrange([]) == -1

    def test_two_elements_decreasing(self):
        """Two elements in decreasing order: violation at index 1."""
        assert can_arrange([5, 3]) == 1

    def test_two_elements_increasing(self):
        """Two elements in increasing order: no violation."""
        assert can_arrange([3, 5]) == -1

    def test_violation_at_start(self):
        """Violation occurs right after the first element."""
        assert can_arrange([5, 1, 2, 3, 4]) == 1

    def test_multiple_violations_returns_largest_index(self):
        """When multiple violations exist, return the largest index."""
        # Violations at indices 2 and 4; should return 4
        assert can_arrange([1, 2, 0, 3, -1]) == 4

    def test_violation_at_last_index(self):
        """The last element breaks the non-decreasing order."""
        assert can_arrange([1, 2, 3, 0]) == 3

    def test_negative_numbers(self):
        """Array with negative numbers."""
        assert can_arrange([-3, -1, -2, 0]) == 2

    def test_sorted_negatives(self):
        """Sorted array of negative numbers: no violation."""
        assert can_arrange([-5, -3, -1, 0, 2]) == -1

    def test_violation_near_end(self):
        """Violation close to the end of a longer array."""
        assert can_arrange([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) == 9

    def test_alternating_pattern(self):
        """Alternating up-down pattern: largest violation index."""
        # [1, 3, 2, 5, 4]: violations at 2 and 4 -> return 4
        assert can_arrange([1, 3, 2, 5, 4]) == 4

    def test_descending_array(self):
        """Fully descending array: every position is a violation."""
        # [5, 4, 3, 2, 1]: violations at 1,2,3,4 -> return 4
        assert can_arrange([5, 4, 3, 2, 1]) == 4

    def test_large_values(self):
        """Test with large integer values."""
        assert can_arrange([1000000, 2000000, 1500000, 3000000]) == 2

    def test_zero_and_positive(self):
        """Mix of zero and positive integers."""
        assert can_arrange([0, 1, 2, 0, 3]) == 3

    def test_three_elements_with_violation(self):
        """Three elements where middle is smaller."""
        assert can_arrange([1, 0, 2]) == 1

    def test_three_elements_sorted(self):
        """Three elements already sorted."""
        assert can_arrange([0, 1, 2]) == -1

    @pytest.mark.parametrize("arr, expected", [
        ([1, 2, 4, 3, 5], 3),
        ([1, 2, 3], -1),
        ([5, 3], 1),
        ([3, 5], -1),
        ([1], -1),
        ([], -1),
        ([1, 3, 2], 2),
        ([2, 1, 3], 1),
        ([1, 2, 3, 2, 4], 3),
        ([10, 20, 30, 25, 40, 35], 5),
    ])
    def test_parametrized_cases(self, arr, expected):
        """Parametrized test cases covering various scenarios."""
        assert can_arrange(arr) == expected
