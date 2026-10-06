import pytest
from solution import intersperse


class TestIntersperse:
    """Unit tests for the intersperse function."""

    def test_empty_list(self):
        """Empty input should return an empty list."""
        assert intersperse([], 4) == []

    def test_single_element(self):
        """A list with one element should return that element unchanged."""
        assert intersperse([1], 4) == [1]

    def test_two_elements(self):
        """Two elements should have the delimiter inserted between them."""
        assert intersperse([1, 2], 4) == [1, 4, 2]

    def test_three_elements(self):
        """Three elements should have delimiters between each pair."""
        assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]

    def test_four_elements(self):
        """Four elements should have three delimiters inserted."""
        assert intersperse([10, 20, 30, 40], 5) == [10, 5, 20, 5, 30, 5, 40]

    def test_delimiter_zero(self):
        """Zero as delimiter should still be inserted correctly."""
        assert intersperse([1, 2, 3], 0) == [1, 0, 2, 0, 3]

    def test_delimiter_negative(self):
        """Negative delimiter should be inserted correctly."""
        assert intersperse([1, 2], -1) == [1, -1, 2]

    def test_delimiter_large(self):
        """Large delimiter value should work correctly."""
        assert intersperse([1, 2], 999999) == [1, 999999, 2]

    def test_negative_numbers_in_list(self):
        """List containing negative numbers should work correctly."""
        assert intersperse([-1, -2, -3], 0) == [-1, 0, -2, 0, -3]

    def test_mixed_positive_negative(self):
        """List with mixed positive and negative numbers."""
        assert intersperse([1, -1, 2], 0) == [1, 0, -1, 0, 2]

    def test_no_modification_of_original(self):
        """The original list should not be modified."""
        original = [1, 2, 3]
        result = intersperse(original, 4)
        assert original == [1, 2, 3]
        assert result == [1, 4, 2, 4, 3]

    def test_docstring_example_1(self):
        """Test from docstring: empty list."""
        assert intersperse([], 4) == []

    def test_docstring_example_2(self):
        """Test from docstring: [1, 2, 3] with delimiter 4."""
        assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]

    def test_larger_list(self):
        """Test with a larger list to ensure correctness at scale."""
        nums = list(range(1, 11))
        expected = []
        for i, n in enumerate(nums):
            expected.append(n)
            if i != len(nums) - 1:
                expected.append(99)
        assert intersperse(nums, 99) == expected

    def test_all_same_elements(self):
        """List with all identical elements."""
        assert intersperse([5, 5, 5], 1) == [5, 1, 5, 1, 5]

    def test_delimiter_equals_element_value(self):
        """Delimiter value equals one of the list elements."""
        assert intersperse([1, 2, 3], 2) == [1, 2, 2, 2, 3]
