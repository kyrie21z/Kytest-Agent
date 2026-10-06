import pytest
from solution import prod_signs


class TestProdSigns_EmptyAndZero:
    """Tests for empty input and zero-containing inputs."""

    def test_empty_array(self):
        """Empty array should return None."""
        assert prod_signs([]) is None

    def test_single_zero(self):
        """Array with a single zero element returns 0."""
        assert prod_signs([0]) == 0

    def test_array_with_zero_and_others(self):
        """Any zero in the array makes the result 0."""
        assert prod_signs([0, 1]) == 0

    def test_array_with_zero_in_middle(self):
        """Zero in the middle still yields 0."""
        assert prod_signs([1, 0, 2]) == 0

    def test_array_with_multiple_zeros(self):
        """Multiple zeros also yield 0."""
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_at_end(self):
        """Zero at the end still yields 0."""
        assert prod_signs([1, 2, 0]) == 0


class TestProdSigns_AllPositive:
    """Tests for arrays containing only positive integers."""

    def test_single_positive(self):
        """Single positive number returns itself."""
        assert prod_signs([5]) == 5

    def test_all_positive(self):
        """All positive numbers: sum of magnitudes, sign product = +1."""
        assert prod_signs([1, 2, 3]) == 6

    def test_example_from_docstring(self):
        """Example from docstring: [1, 2, 2, -4] -> -9."""
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_larger_all_positive(self):
        """Larger array of all positives."""
        assert prod_signs([1, 2, 3, 4, 5]) == 15

    def test_repeated_positive_values(self):
        """Repeated positive values."""
        assert prod_signs([3, 3, 3]) == 9


class TestProdSigns_AllNegative:
    """Tests for arrays containing only negative integers."""

    def test_single_negative(self):
        """Single negative number returns its negated magnitude."""
        assert prod_signs([-3]) == -3

    def test_two_negatives_even_count(self):
        """Two negatives: sign product = +1, result is sum of magnitudes."""
        assert prod_signs([-1, -2]) == 3

    def test_three_negatives_odd_count(self):
        """Three negatives: sign product = -1, result is negative sum."""
        assert prod_signs([-1, -2, -3]) == -6

    def test_four_negatives_even_count(self):
        """Four negatives: sign product = +1."""
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_five_negatives_odd_count(self):
        """Five negatives: sign product = -1."""
        assert prod_signs([-1, -2, -3, -4, -5]) == -15


class TestProdSigns_MixedSigns:
    """Tests for arrays with mixed positive and negative integers."""

    def test_one_negative(self):
        """One negative: sign product = -1."""
        assert prod_signs([1, -2, 3]) == -6

    def test_two_negatives(self):
        """Two negatives: sign product = +1."""
        assert prod_signs([-1, -2, 3]) == 6

    def test_three_negatives(self):
        """Three negatives: sign product = -1."""
        assert prod_signs([-1, -2, -3, 4]) == -10

    def test_alternating_signs(self):
        """Alternating positive/negative."""
        assert prod_signs([1, -2, 3, -4]) == 10

    def test_mixed_with_large_values(self):
        """Mixed signs with larger values."""
        assert prod_signs([10, -20, 30]) == -60

    def test_single_element_positive(self):
        """Single positive element."""
        assert prod_signs([7]) == 7

    def test_single_element_negative(self):
        """Single negative element."""
        assert prod_signs([-7]) == -7


class TestProdSigns_BoundaryCases:
    """Tests for edge/boundary values."""

    def test_largest_single_value(self):
        """Large positive value."""
        assert prod_signs([100]) == 100

    def test_largest_single_negative(self):
        """Large negative value."""
        assert prod_signs([-100]) == -100

    def test_many_elements_all_same(self):
        """Many elements, all the same positive value."""
        assert prod_signs([1] * 10) == 10

    def test_many_elements_all_same_negative(self):
        """Many elements, all the same negative value."""
        assert prod_signs([-1] * 10) == 10  # even count => sign = +1

    def test_many_elements_odd_negative_count(self):
        """Many elements, odd count of negatives."""
        assert prod_signs([-1] * 9) == -9  # odd count => sign = -1

    def test_value_of_one(self):
        """Array with 1s."""
        assert prod_signs([1, 1, 1]) == 3

    def test_value_of_negative_one(self):
        """Array with -1s."""
        assert prod_signs([-1, -1]) == 2

    def test_magnitude_one_mixed(self):
        """Mix of 1 and -1."""
        assert prod_signs([1, -1]) == -2


class TestProdSigns_DocstringExamples:
    """Directly verify the examples given in the docstring."""

    def test_docstring_example_1(self):
        """>>> prod_signs([1, 2, 2, -4]) == -9"""
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_docstring_example_2(self):
        """>>> prod_signs([0, 1]) == 0"""
        assert prod_signs([0, 1]) == 0

    def test_docstring_example_3(self):
        """>>> prod_signs([]) == None"""
        assert prod_signs([]) is None
