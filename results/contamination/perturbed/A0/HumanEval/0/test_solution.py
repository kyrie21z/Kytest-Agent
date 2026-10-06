import pytest
from solution import fn_00_x


class TestFn00XBasicCases:
    """Test basic positive and negative scenarios."""

    def test_no_pair_closer_than_threshold(self):
        """All numbers are at least threshold apart."""
        assert fn_00_x([1.0, 2.0, 3.0], 0.5) is False

    def test_pair_closer_than_threshold(self):
        """At least one pair is closer than threshold."""
        assert fn_00_x([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) is True

    def test_exact_threshold_difference(self):
        """Difference exactly equals threshold — should NOT trigger (strictly less)."""
        assert fn_00_x([1.0, 2.0], 1.0) is False

    def test_difference_less_than_threshold(self):
        """Difference is just below threshold."""
        assert fn_00_x([1.0, 1.99], 1.0) is True


class TestFn00XEdgeCases:
    """Test edge cases for input size and values."""

    def test_empty_list(self):
        """Empty list has no pairs, should return False."""
        assert fn_00_x([], 1.0) is False

    def test_single_element(self):
        """Single element has no pairs, should return False."""
        assert fn_00_x([42.0], 0.5) is False

    def test_two_elements_closer(self):
        """Two elements where difference < threshold."""
        assert fn_00_x([1.0, 1.5], 1.0) is True

    def test_two_elements_not_closer(self):
        """Two elements where difference >= threshold."""
        assert fn_00_x([1.0, 3.0], 1.0) is False

    def test_two_elements_equal(self):
        """Two identical elements have difference 0 < any positive threshold."""
        assert fn_00_x([5.0, 5.0], 1.0) is True


class TestFn00XWithDuplicates:
    """Test behavior when the list contains duplicate values."""

    def test_all_same_values(self):
        """All elements identical; difference is 0."""
        assert fn_00_x([3.0, 3.0, 3.0, 3.0], 0.1) is True

    def test_some_duplicates(self):
        """List with some duplicates among distinct values."""
        assert fn_00_x([1.0, 2.0, 2.0, 5.0], 0.5) is True

    def test_duplicates_but_threshold_zero(self):
        """Duplicate values with threshold 0 — difference 0 is not < 0."""
        assert fn_00_x([1.0, 1.0], 0.0) is False

    def test_no_duplicates_and_not_closer(self):
        """No duplicates and all pairs far enough apart."""
        assert fn_00_x([1.0, 3.0, 5.0, 7.0], 1.5) is False


class TestFn00XSpecialThresholds:
    """Test with special threshold values."""

    def test_negative_threshold(self):
        """Negative threshold: no non-negative difference can be < negative."""
        assert fn_00_x([1.0, 2.0], -0.5) is False

    def test_zero_threshold(self):
        """Zero threshold: only exact duplicates qualify."""
        assert fn_00_x([1.0, 2.0, 3.0], 0.0) is False

    def test_zero_threshold_with_duplicates(self):
        """Zero threshold with duplicate values."""
        assert fn_00_x([1.0, 1.0, 3.0], 0.0) is False

    def test_very_large_threshold(self):
        """Very large threshold: almost any pair qualifies."""
        assert fn_00_x([1.0, 100.0], 200.0) is True

    def test_very_small_positive_threshold(self):
        """Very small positive threshold: only very close pairs qualify."""
        assert fn_00_x([1.0, 1.0000001], 0.000001) is True
        assert fn_00_x([1.0, 1.0000001], 0.00000001) is False


class TestFn00XUnsortedInput:
    """Test that unsorted input is handled correctly."""

    def test_unsorted_list(self):
        """Close pair appears in unsorted order."""
        # sorted: [1.0, 1.5, 3.0, 5.0] -> diff 0.5 < 0.6
        assert fn_00_x([5.0, 1.0, 3.0, 1.5], 0.6) is True

    def test_reverse_sorted(self):
        """Reverse-sorted list with a close pair."""
        # sorted: [1.0, 1.1, 3.0, 4.0, 5.0] -> diff 0.1 < 0.5
        assert fn_00_x([5.0, 4.0, 3.0, 1.1, 1.0], 0.5) is True

    def test_random_order(self):
        """Randomly ordered list with a close pair."""
        # sorted: [1.0, 1.2, 5.0, 8.0, 10.0] -> diff 0.2 < 0.5
        assert fn_00_x([10.0, 1.0, 5.0, 1.2, 8.0], 0.5) is True


class TestFn00XMixedNumbers:
    """Test with various numeric types and signs."""

    def test_negative_numbers(self):
        """List of negative numbers with a close pair."""
        # sorted: [-5.0, -4.9, -3.0] -> diff 0.1 < 0.5
        assert fn_00_x([-5.0, -4.9, -3.0], 0.5) is True

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers with a close pair."""
        # sorted: [-0.1, 0.0, 1.0] -> diff 0.1 < 0.5
        assert fn_00_x([-1.0, -0.1, 0.0, 1.0], 0.5) is True

    def test_close_negative_pair(self):
        """Close pair among negative numbers."""
        assert fn_00_x([-1.0, -1.1, 5.0], 0.2) is True

    def test_integers(self):
        """Integer inputs (should work as floats)."""
        assert fn_00_x([1, 2, 3], 1) is False
        assert fn_00_x([1, 2, 3], 2) is True

    def test_large_values(self):
        """Large magnitude numbers."""
        assert fn_00_x([1e10, 1e10 + 0.5, 2e10], 1.0) is True

    def test_small_decimal_values(self):
        """Small decimal values with a close pair."""
        # sorted: [0.001, 0.0015, 0.003] -> diff 0.0005 < 0.001
        assert fn_00_x([0.001, 0.0015, 0.003], 0.001) is True


class TestFn00XDoctests:
    """Verify the examples from the docstring pass."""

    def test_docstring_example_1(self):
        assert fn_00_x([1.0, 2.0, 3.0], 0.5) is False

    def test_docstring_example_2(self):
        assert fn_00_x([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) is True
