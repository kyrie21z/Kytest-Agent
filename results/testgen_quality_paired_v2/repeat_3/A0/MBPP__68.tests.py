import pytest
from solution import is_Monotonic


class TestIsMonotonic:
    """Unit tests for the is_Monotonic function."""

    # --- Edge cases ---

    def test_empty_array(self):
        """An empty array is vacuously monotonic."""
        assert is_Monotonic([]) is True

    def test_single_element(self):
        """A single-element array is monotonic."""
        assert is_Monotonic([1]) is True

    def test_two_equal_elements(self):
        """Two identical elements form a monotonic array."""
        assert is_Monotonic([3, 3]) is True

    def test_two_increasing_elements(self):
        """Two elements in ascending order are monotonic."""
        assert is_Monotonic([1, 2]) is True

    def test_two_decreasing_elements(self):
        """Two elements in descending order are monotonic."""
        assert is_Monotonic([2, 1]) is True

    # --- Monotonically non-decreasing arrays ---

    def test_strictly_increasing(self):
        """A strictly increasing array is monotonic."""
        assert is_Monotonic([1, 2, 3, 4, 5]) is True

    def test_non_decreasing_with_duplicates(self):
        """A non-decreasing array with duplicate values is monotonic."""
        assert is_Monotonic([1, 2, 2, 3, 4]) is True

    def test_all_same_elements(self):
        """An array where all elements are equal is monotonic."""
        assert is_Monotonic([5, 5, 5, 5]) is True

    def test_non_decreasing_large(self):
        """Larger non-decreasing array."""
        assert is_Monotonic(list(range(100))) is True

    # --- Monotonically non-increasing arrays ---

    def test_strictly_decreasing(self):
        """A strictly decreasing array is monotonic."""
        assert is_Monotonic([5, 4, 3, 2, 1]) is True

    def test_non_increasing_with_duplicates(self):
        """A non-increasing array with duplicate values is monotonic."""
        assert is_Monotonic([5, 4, 4, 3, 2]) is True

    def test_non_increasing_large(self):
        """Larger non-increasing array."""
        assert is_Monotonic(list(range(100, 0, -1))) is True

    # --- Negative numbers ---

    def test_negative_numbers_increasing(self):
        """Negative numbers in increasing order are monotonic."""
        assert is_Monotonic([-5, -3, -1, 0, 2]) is True

    def test_negative_numbers_decreasing(self):
        """Negative numbers in decreasing order are monotonic."""
        assert is_Monotonic([2, 0, -1, -3, -5]) is True

    def test_mixed_positive_negative_increasing(self):
        """Mixed positive and negative numbers in increasing order."""
        assert is_Monotonic([-3, -1, 0, 1, 2]) is True

    def test_mixed_positive_negative_decreasing(self):
        """Mixed positive and negative numbers in decreasing order."""
        assert is_Monotonic([3, 1, 0, -1, -2]) is True

    # --- Non-monotonic arrays ---

    def test_up_then_down(self):
        """Array that increases then decreases is not monotonic."""
        assert is_Monotonic([1, 3, 2]) is False

    def test_down_then_up(self):
        """Array that decreases then increases is not monotonic."""
        assert is_Monotonic([3, 1, 2]) is False

    def test_v_shape(self):
        """V-shaped array is not monotonic."""
        assert is_Monotonic([3, 2, 1, 2, 3]) is False

    def test_inverted_v_shape(self):
        """Inverted V-shaped array is not monotonic."""
        assert is_Monotonic([1, 2, 3, 2, 1]) is False

    def test_random_order(self):
        """Randomly ordered array is not monotonic."""
        assert is_Monotonic([1, 3, 2, 4, 1]) is False

    def test_multiple_peaks_and_valleys(self):
        """Array with multiple peaks and valleys is not monotonic."""
        assert is_Monotonic([5, 1, 4, 2, 3]) is False

    def test_plateau_then_change(self):
        """Array with a plateau followed by a change in direction."""
        assert is_Monotonic([1, 2, 2, 1]) is False

    def test_plateau_then_opposite_change(self):
        """Array with a plateau followed by opposite direction change."""
        assert is_Monotonic([3, 2, 2, 3]) is False

    # --- Parameterized tests ---

    @pytest.mark.parametrize("array, expected", [
        ([], True),
        ([1], True),
        ([1, 2], True),
        ([2, 1], True),
        ([1, 1], True),
        ([1, 2, 3, 4, 5], True),
        ([5, 4, 3, 2, 1], True),
        ([1, 1, 1, 1], True),
        ([1, 2, 2, 3], True),
        ([5, 5, 4, 3], True),
        ([1, 3, 2], False),
        ([3, 1, 2], False),
        ([1, 2, 3, 2, 1], False),
        ([1, 3, 2, 4, 1], False),
        ([-1, -2, -3], True),
        ([-3, -2, -1], True),
        ([-1, 0, 1, 0, -1], False),
    ])
    def test_parametrized(self, array, expected):
        """Parametrized test covering a wide range of inputs."""
        assert is_Monotonic(array) is expected
