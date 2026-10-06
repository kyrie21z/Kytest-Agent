import pytest
from solution import fn_01_x


class TestFn01X:
    """Unit tests for fn_01_x function."""

    def test_empty_list(self):
        """Empty input should return an empty list."""
        assert fn_01_x([], 4) == []

    def test_single_element(self):
        """A single-element list should be returned unchanged."""
        assert fn_01_x([1], 4) == [1]

    def test_two_elements(self):
        """Two elements should have the delimiter inserted between them."""
        assert fn_01_x([1, 2], 4) == [1, 4, 2]

    def test_three_elements(self):
        """Three elements should have delimiters between each pair."""
        assert fn_01_x([1, 2, 3], 4) == [1, 4, 2, 4, 3]

    def test_multiple_elements(self):
        """Multiple elements should have delimiters between all consecutive pairs."""
        assert fn_01_x([1, 2, 3, 4], 5) == [1, 5, 2, 5, 3, 5, 4]

    def test_negative_delimiter(self):
        """Negative delimiter should be inserted correctly."""
        assert fn_01_x([1, 2, 3], -1) == [1, -1, 2, -1, 3]

    def test_zero_delimiter(self):
        """Zero as delimiter should be inserted correctly."""
        assert fn_01_x([1, 2, 3], 0) == [1, 0, 2, 0, 3]

    def test_large_delimiter(self):
        """Large delimiter value should work correctly."""
        assert fn_01_x([1, 2], 999999) == [1, 999999, 2]

    def test_negative_numbers_in_list(self):
        """List containing negative numbers should work correctly."""
        assert fn_01_x([-1, -2, -3], 0) == [-1, 0, -2, 0, -3]

    def test_mixed_positive_negative_numbers(self):
        """List with mixed positive and negative numbers."""
        assert fn_01_x([1, -2, 3], 0) == [1, 0, -2, 0, 3]

    def test_duplicate_values(self):
        """List with duplicate values should insert delimiters correctly."""
        assert fn_01_x([1, 1, 1], 5) == [1, 5, 1, 5, 1]

    def test_all_same_elements(self):
        """List where all elements are identical."""
        assert fn_01_x([7, 7, 7, 7], 0) == [7, 0, 7, 0, 7, 0, 7]

    def test_delimiter_equals_element_value(self):
        """When delimiter equals an element value, behavior should still be correct."""
        assert fn_01_x([1, 2, 3], 2) == [1, 2, 2, 2, 3]

    def test_five_elements(self):
        """Five elements should produce four delimiters."""
        result = fn_01_x([10, 20, 30, 40, 50], 99)
        expected = [10, 99, 20, 99, 30, 99, 40, 99, 50]
        assert result == expected

    def test_return_type_is_list(self):
        """The return value should always be a list."""
        assert isinstance(fn_01_x([], 1), list)
        assert isinstance(fn_01_x([1], 1), list)
        assert isinstance(fn_01_x([1, 2], 1), list)

    def test_original_list_not_modified(self):
        """The original input list should not be modified."""
        original = [1, 2, 3]
        fn_01_x(original, 5)
        assert original == [1, 2, 3]

    @pytest.mark.parametrize(
        "numbers,delimeter,expected",
        [
            ([], 0, []),
            ([5], 0, [5]),
            ([1, 2], 0, [1, 0, 2]),
            ([1, 2, 3], 0, [1, 0, 2, 0, 3]),
            ([1, 2, 3, 4, 5], 1, [1, 1, 2, 1, 3, 1, 4, 1, 5]),
            ([-5, -3, -1, 0, 2], -10, [-5, -10, -3, -10, -1, -10, 0, -10, 2]),
        ],
    )
    def test_parametrized(self, numbers, delimeter, expected):
        """Parametrized tests covering various combinations."""
        assert fn_01_x(numbers, delimeter) == expected
