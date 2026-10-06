import pytest
from solution import intersperse


class TestIntersperse:
    """Tests for the intersperse function."""

    def test_empty_list(self):
        """Empty input should return an empty list."""
        assert intersperse([], 4) == []

    def test_single_element(self):
        """A single-element list should be returned unchanged."""
        assert intersperse([1], 5) == [1]

    def test_two_elements(self):
        """Two elements should have the delimiter inserted between them."""
        assert intersperse([1, 2], 3) == [1, 3, 2]

    def test_three_elements(self):
        """Three elements should have delimiters between each pair."""
        assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]

    def test_multiple_elements(self):
        """Multiple elements should have delimiters between all consecutive pairs."""
        assert intersperse([1, 2, 3, 4], 0) == [1, 0, 2, 0, 3, 0, 4]

    def test_delimiter_zero(self):
        """Delimiter value of zero should still be inserted correctly."""
        assert intersperse([1, 2, 3], 0) == [1, 0, 2, 0, 3]

    def test_delimiter_negative(self):
        """Negative delimiter values should work correctly."""
        assert intersperse([1, 2, 3], -1) == [1, -1, 2, -1, 3]

    def test_delimiter_large(self):
        """Large delimiter values should work correctly."""
        assert intersperse([1, 2], 999999) == [1, 999999, 2]

    def test_all_same_elements(self):
        """List with identical elements should still insert delimiters."""
        assert intersperse([7, 7, 7], 3) == [7, 3, 7, 3, 7]

    def test_negative_numbers_in_list(self):
        """Input list containing negative numbers should work correctly."""
        assert intersperse([-1, -2, -3], 0) == [-1, 0, -2, 0, -3]

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers in the list."""
        assert intersperse([1, -1, 2, -2], 0) == [1, 0, -1, 0, 2, 0, -2]

    def test_delimiter_equals_element_value(self):
        """When delimiter equals an element value, behavior should still be correct."""
        assert intersperse([1, 2, 3], 2) == [1, 2, 2, 2, 3]

    def test_five_elements(self):
        """Test with five elements to verify scaling."""
        result = intersperse([10, 20, 30, 40, 50], -1)
        expected = [10, -1, 20, -1, 30, -1, 40, -1, 50]
        assert result == expected

    def test_return_type(self):
        """Ensure the return type is a list."""
        result = intersperse([1, 2], 3)
        assert isinstance(result, list)

    def test_no_modification_of_input(self):
        """The original input list should not be modified."""
        original = [1, 2, 3]
        original_copy = original.copy()
        intersperse(original, 5)
        assert original == original_copy
