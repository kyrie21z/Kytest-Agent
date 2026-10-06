import pytest
from solution import filter_integers


class TestFilterIntegers:
    """Tests for the filter_integers function."""

    def test_basic_mixed_list(self):
        """Test filtering a list with mixed types."""
        result = filter_integers(['a', 3.14, 5])
        assert result == [5]

    def test_list_with_multiple_types(self):
        """Test filtering a list containing various Python types."""
        result = filter_integers([1, 2, 3, 'abc', {}, []])
        assert result == [1, 2, 3]

    def test_empty_list(self):
        """Test filtering an empty list."""
        result = filter_integers([])
        assert result == []

    def test_list_with_only_integers(self):
        """Test filtering a list that contains only integers."""
        result = filter_integers([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_list_with_no_integers(self):
        """Test filtering a list that contains no integers."""
        result = filter_integers(['a', 'b', 3.14, None, {}, []])
        assert result == []

    def test_booleans_not_included(self):
        """Test that boolean values are not included (bool is subclass of int)."""
        result = filter_integers([True, False, 1, 0])
        assert result == [1, 0]

    def test_negative_integers(self):
        """Test that negative integers are correctly filtered."""
        result = filter_integers([-1, -2, -3, 'a', 4])
        assert result == [-1, -2, -3, 4]

    def test_zero_is_included(self):
        """Test that zero is correctly included as an integer."""
        result = filter_integers([0, 'zero', 1])
        assert result == [0, 1]

    def test_large_integers(self):
        """Test that large integers are correctly filtered."""
        result = filter_integers([10**100, 'big', 42])
        assert result == [10**100, 42]

    def test_floats_not_included(self):
        """Test that float values are not included."""
        result = filter_integers([1.0, 2.5, 3, 4.0])
        assert result == [3]

    def test_strings_not_included(self):
        """Test that string values are not included."""
        result = filter_integers(['1', '2', '3', 4])
        assert result == [4]

    def test_none_not_included(self):
        """Test that None values are not included."""
        result = filter_integers([None, 1, None, 2])
        assert result == [1, 2]

    def test_dicts_and_lists_not_included(self):
        """Test that dict and list values are not included."""
        result = filter_integers([{}, [], {1: 2}, [3], 4])
        assert result == [4]

    def test_tuples_not_included(self):
        """Test that tuple values are not included."""
        result = filter_integers([(1, 2), 3, (4,)])
        assert result == [3]

    def test_preserves_order(self):
        """Test that the order of integers is preserved."""
        result = filter_integers([5, 'a', 3, 'b', 1, 'c'])
        assert result == [5, 3, 1]

    def test_complex_objects_not_included(self):
        """Test that complex number objects are not included."""
        result = filter_integers([1 + 2j, 3, 4 + 5j])
        assert result == [3]

    def test_single_integer(self):
        """Test filtering a list with a single integer."""
        result = filter_integers([42])
        assert result == [42]

    def test_single_non_integer(self):
        """Test filtering a list with a single non-integer."""
        result = filter_integers(['hello'])
        assert result == []

    def test_duplicate_integers(self):
        """Test that duplicate integers are preserved."""
        result = filter_integers([1, 2, 1, 3, 2])
        assert result == [1, 2, 1, 3, 2]

    def test_all_different_types(self):
        """Test filtering a list with many different types."""
        values = [
            42,           # int -> include
            'text',       # str -> exclude
            3.14,         # float -> exclude
            True,         # bool -> exclude
            None,         # NoneType -> exclude
            [1, 2],       # list -> exclude
            {'key': 'val'},  # dict -> exclude
            (1, 2),       # tuple -> exclude
            set([1]),     # set -> exclude
            b'bytes',     # bytes -> exclude
            0,            # int -> include
            -7,           # int -> include
        ]
        result = filter_integers(values)
        assert result == [42, 0, -7]
