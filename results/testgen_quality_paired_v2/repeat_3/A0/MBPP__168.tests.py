import pytest
from solution import frequency


class TestFrequencyBasic:
    """Test basic functionality of the frequency function."""

    def test_single_occurrence(self):
        assert frequency([1, 2, 3, 4, 5], 3) == 1

    def test_multiple_occurrences(self):
        assert frequency([1, 2, 2, 3, 2, 4], 2) == 3

    def test_no_occurrences(self):
        assert frequency([1, 2, 3, 4, 5], 6) == 0

    def test_all_elements_match(self):
        assert frequency([7, 7, 7, 7], 7) == 4


class TestFrequencyEdgeCases:
    """Test edge cases for the frequency function."""

    def test_empty_list(self):
        assert frequency([], 5) == 0

    def test_single_element_matching(self):
        assert frequency([42], 42) == 1

    def test_single_element_not_matching(self):
        assert frequency([42], 99) == 0

    def test_two_identical_elements(self):
        assert frequency([3, 3], 3) == 2

    def test_two_different_elements(self):
        assert frequency([1, 2], 3) == 0


class TestFrequencyNegativeNumbers:
    """Test with negative numbers."""

    def test_negative_target(self):
        assert frequency([-1, -2, -3, -2, -4], -2) == 2

    def test_negative_in_mixed_list(self):
        assert frequency([1, -1, 2, -1, 3], -1) == 2

    def test_all_negative(self):
        assert frequency([-5, -5, -5], -5) == 3


class TestFrequencyFloats:
    """Test with floating point numbers."""

    def test_float_target(self):
        assert frequency([1.5, 2.5, 3.5, 2.5], 2.5) == 2

    def test_float_no_match(self):
        assert frequency([1.1, 2.2, 3.3], 4.4) == 0

    def test_zero_float(self):
        assert frequency([0.0, 1.0, 0.0], 0.0) == 2


class TestFrequencyLargeLists:
    """Test with larger lists."""

    def test_large_list(self):
        lst = [1] * 1000 + [2] * 500
        assert frequency(lst, 1) == 1000
        assert frequency(lst, 2) == 500
        assert frequency(lst, 3) == 0

    def test_many_occurrences(self):
        lst = [42] * 10000
        assert frequency(lst, 42) == 10000


class TestFrequencyStringLikeBehavior:
    """Test that the function works correctly with various types."""

    def test_string_elements(self):
        assert frequency(["a", "b", "a", "c", "a"], "a") == 3

    def test_string_no_match(self):
        assert frequency(["x", "y", "z"], "w") == 0

    def test_mixed_types_no_match(self):
        # Numbers and strings should not match each other
        assert frequency([1, 2, "1", "2"], 1) == 1
        assert frequency([1, 2, "1", "2"], "1") == 1


class TestFrequencyReturnTypes:
    """Test that return type is always an integer."""

    def test_returns_int_for_empty(self):
        result = frequency([], 1)
        assert isinstance(result, int)
        assert result == 0

    def test_returns_int_for_matches(self):
        result = frequency([1, 1, 1], 1)
        assert isinstance(result, int)
        assert result == 3
