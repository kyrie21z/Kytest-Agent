import pytest
from solution import sum_product


class TestSumProduct:
    """Unit tests for the sum_product function."""

    def test_empty_list(self):
        """Empty list should return (0, 1)."""
        assert sum_product([]) == (0, 1)

    def test_single_element(self):
        """A single-element list should return (n, n)."""
        assert sum_product([5]) == (5, 5)

    def test_single_zero(self):
        """A list with a single zero should return (0, 0)."""
        assert sum_product([0]) == (0, 0)

    def test_two_elements(self):
        """Two elements should compute correct sum and product."""
        assert sum_product([2, 3]) == (5, 6)

    def test_multiple_positive_integers(self):
        """Multiple positive integers should return correct sum and product."""
        assert sum_product([1, 2, 3, 4]) == (10, 24)

    def test_all_ones(self):
        """List of all ones: sum = count, product = 1."""
        assert sum_product([1, 1, 1, 1]) == (4, 1)

    def test_negative_numbers(self):
        """Negative numbers should be handled correctly."""
        assert sum_product([-1, -2, -3]) == (-6, -6)

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers."""
        assert sum_product([1, -1, 2, -2]) == (0, 4)

    def test_with_zero_in_list(self):
        """If any element is zero, product should be zero."""
        assert sum_product([1, 2, 0, 4]) == (7, 0)

    def test_large_numbers(self):
        """Large integers should still work correctly."""
        assert sum_product([100, 200, 300]) == (600, 6_000_000)

    def test_duplicate_elements(self):
        """List with duplicate values."""
        assert sum_product([3, 3, 3]) == (9, 27)

    def test_all_negative(self):
        """All negative numbers with even count -> positive product."""
        assert sum_product([-2, -3]) == (-5, 6)

    def test_all_negative_odd_count(self):
        """All negative numbers with odd count -> negative product."""
        assert sum_product([-2, -3, -4]) == (-9, -24)

    def test_single_negative(self):
        """Single negative number."""
        assert sum_product([-7]) == (-7, -7)

    def test_many_zeros(self):
        """Multiple zeros: sum = 0, product = 0."""
        assert sum_product([0, 0, 0]) == (0, 0)

    def test_alternating_signs(self):
        """Alternating positive and negative values."""
        assert sum_product([1, -2, 3, -4, 5]) == (3, 120)

    def test_type_consistency(self):
        """Return type should always be a tuple of two ints."""
        result = sum_product([1, 2, 3])
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], int)
        assert isinstance(result[1], int)
