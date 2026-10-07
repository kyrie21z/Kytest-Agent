import pytest
from solution import max_product


class TestMaxProductBasic:
    """Tests for basic functionality of max_product."""

    def test_single_element(self):
        """A single-element array returns that element."""
        assert max_product([5]) == 5

    def test_two_elements_increasing(self):
        """Two elements in increasing order return their product."""
        assert max_product([2, 3]) == 6

    def test_two_elements_decreasing(self):
        """Two elements in decreasing order return the larger one."""
        assert max_product([3, 2]) == 3

    def test_three_elements_increasing(self):
        """Three elements in increasing order return their product."""
        assert max_product([1, 2, 3]) == 6

    def test_simple_case(self):
        """Standard mixed case."""
        assert max_product([1, 3, 2, 4]) == 8

    def test_all_same_elements(self):
        """Array with all identical elements treats them as non-decreasing,
        so the product of all elements is returned."""
        # [4, 4, 4] -> non-decreasing subseqs include [4,4,4]->prod=64
        assert max_product([4, 4, 4]) == 64


class TestMaxProductIncreasingSubsequences:
    """Tests focused on contiguous increasing subsequences."""

    def test_increasing_then_decreasing(self):
        """Longest increasing prefix determines the result."""
        # [1, 2, 3, 2, 1] -> increasing subseqs: [1,2,3], [2], [3,2]break, [2,1]break, [1]
        # Products: 6, 2, 3, 2, 1 => max = 6
        assert max_product([1, 2, 3, 2, 1]) == 6

    def test_decreasing_then_increasing(self):
        """Handles decreasing start followed by increasing."""
        # [5, 4, 1, 2, 3] -> increasing subseqs: [5], [4], [1,2,3]
        # Products: 5, 4, 6 => max = 6
        assert max_product([5, 4, 1, 2, 3]) == 6

    def test_multiple_increasing_segments(self):
        """Picks the segment with the highest product."""
        # [1, 2, 10, 1, 2, 3]
        # Segments: [1,2,10]->prod=20, [1,2,3]->prod=6
        assert max_product([1, 2, 10, 1, 2, 3]) == 20

    def test_ascending_sequence(self):
        """Fully ascending sequence returns product of all elements."""
        assert max_product([1, 2, 3, 4, 5]) == 120

    def test_descending_sequence(self):
        """Fully descending sequence returns the first (largest) element."""
        assert max_product([5, 4, 3, 2, 1]) == 5


class TestMaxProductEdgeCases:
    """Tests for edge cases and special values."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError since max() on empty sequence fails."""
        with pytest.raises(ValueError):
            max_product([])

    def test_zeros_in_array(self):
        """Zeros in the array are handled correctly."""
        # [0, 1, 2] -> increasing subseqs: [0,1,2]->prod=0, [1,2]->prod=2, [2]->prod=2
        assert max_product([0, 1, 2]) == 2

    def test_zero_as_only_element(self):
        """Single zero returns zero."""
        assert max_product([0]) == 0

    def test_negative_numbers(self):
        """Negative numbers are included in products.
        [-3, -2, -1] is non-decreasing, so products accumulate from each start point:
        i=0: prod=-3, then (-3)*(-2)=6, then 6*(-1)=-6
        i=1: prod=-2, then (-2)*(-1)=2
        i=2: prod=-1
        max([-3, 6, 2]) = 6"""
        assert max_product([-3, -2, -1]) == 6

    def test_mixed_positive_and_negative(self):
        """Mixed positive and negative values."""
        # [-1, 2, 3, -2, 4]
        # Subseqs: [-1,2,3]->prod=-6, [2,3]->prod=6, [3], [-2,4]->prod=-8, [4]
        assert max_product([-1, 2, 3, -2, 4]) == 6

    def test_large_values(self):
        """Test with large numbers to ensure no overflow issues."""
        assert max_product([10, 20, 30]) == 6000

    def test_duplicate_adjacent_elements(self):
        """Adjacent equal elements are treated as non-increasing (continue)."""
        # [1, 2, 2, 3]
        # Non-decreasing: [1,2,2,3]->prod=12
        assert max_product([1, 2, 2, 3]) == 12

    def test_all_zeros(self):
        """Array of all zeros."""
        assert max_product([0, 0, 0]) == 0

    def test_two_equal_elements(self):
        """Two equal elements are treated as non-decreasing, product is returned."""
        # [5, 5] -> non-decreasing subseq [5,5]->prod=25
        assert max_product([5, 5]) == 25


class TestMaxProductLargerArrays:
    """Tests with larger arrays to verify correctness."""

    def test_alternating_pattern(self):
        """Alternating up-down pattern."""
        # [1, 5, 2, 6, 3, 7]
        # Subseqs: [1,5]->prod=5, [5], [2,6]->prod=12, [6], [3,7]->prod=21, [7]
        assert max_product([1, 5, 2, 6, 3, 7]) == 21

    def test_long_increasing_sequence(self):
        """Long increasing sequence."""
        arr = list(range(1, 11))  # [1, 2, ..., 10]
        expected = 3628800  # 10!
        assert max_product(arr) == expected

    def test_peak_in_middle(self):
        """Peak value in the middle of the array."""
        # [1, 2, 100, 2, 1]
        # Subseqs: [1,2,100]->prod=200, [2,100]->prod=200, [100], [2,1]break, [1]
        assert max_product([1, 2, 100, 2, 1]) == 200

    def test_valley_in_middle(self):
        """Valley (minimum) in the middle of the array."""
        # [5, 4, 1, 2, 3]
        # Subseqs: [5], [4], [1,2,3]->prod=6, [2,3]->prod=6, [3]
        assert max_product([5, 4, 1, 2, 3]) == 6


class TestMaxProductReturnTypes:
    """Tests to verify return types."""

    def test_returns_integer(self):
        """Result should be an integer."""
        result = max_product([2, 3, 4])
        assert isinstance(result, int)

    def test_returns_integer_for_single_element(self):
        """Single element should return that integer."""
        result = max_product([42])
        assert isinstance(result, int)
        assert result == 42
