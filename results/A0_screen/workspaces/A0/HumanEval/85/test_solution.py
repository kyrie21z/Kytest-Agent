import pytest
from solution import add


class TestAdd:
    """Unit tests for the add() function."""

    # --- Basic functionality ---

    def test_example_from_docstring(self):
        """Test case from the docstring: [4, 2, 6, 7] => 2"""
        assert add([4, 2, 6, 7]) == 2

    def test_single_element(self):
        """Single element list: index 0 is even index, so nothing to sum."""
        assert add([3]) == 0

    def test_two_elements(self):
        """Only index 1 is an odd index. lst[1]=2 is even => sum=2."""
        assert add([1, 2]) == 2

    def test_two_elements_odd_at_odd_index(self):
        """lst[1]=3 is odd => not added."""
        assert add([1, 3]) == 0

    def test_three_elements(self):
        """Odd indices: 1. lst[1]=4 is even => sum=4."""
        assert add([1, 4, 3]) == 4

    def test_four_elements_all_even_at_odd_indices(self):
        """Odd indices: 1, 3. Both lst[1]=2 and lst[3]=6 are even => 2+6=8."""
        assert add([1, 2, 3, 6]) == 8

    def test_four_elements_nothing_even_at_odd_indices(self):
        """Odd indices: 1, 3. lst[1]=3 and lst[3]=7 are odd => 0."""
        assert add([1, 3, 5, 7]) == 0

    # --- Negative numbers ---

    def test_negative_even_at_odd_index(self):
        """Negative even number at odd index should be included."""
        assert add([1, -2, 3, 4]) == 2  # -2 + 4 = 2

    def test_negative_even_only(self):
        """All values negative; only those at odd indices and even."""
        assert add([1, -4, 3, -6]) == -10  # -4 + -6 = -10

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative even numbers at odd indices."""
        assert add([0, -2, 0, 4]) == 2  # -2 + 4 = 2

    # --- Zero handling ---

    def test_zero_at_odd_index(self):
        """Zero is even, so it should be included."""
        assert add([1, 0, 3, 0]) == 0

    def test_all_zeros(self):
        """All zeros: zero is even, all at odd indices contribute 0."""
        assert add([0, 0, 0, 0]) == 0

    # --- Larger lists ---

    def test_longer_list(self):
        """Odd indices: 1, 3, 5, 7. Even values: 2, 6, 10, 14 => 32."""
        assert add([0, 2, 1, 6, 2, 9, 3, 14]) == 22  # 2 + 6 + 14 = 22

    def test_alternating_pattern(self):
        """Pattern: odd, even, odd, even, ..."""
        # Odd indices: 1, 3, 5 => values 2, 4, 6 => sum = 12
        assert add([1, 2, 3, 4, 5, 6]) == 12

    def test_even_values_only_at_even_indices(self):
        """Even values exist but only at even indices => nothing summed."""
        assert add([2, 1, 4, 3, 6, 5]) == 0

    def test_odd_values_only_at_odd_indices(self):
        """Odd values at odd indices => nothing summed."""
        assert add([0, 1, 2, 3, 4, 5]) == 0

    # --- Edge cases ---

    def test_empty_list_raises_or_returns(self):
        """The docstring says non-empty list; test behavior with empty."""
        # Based on implementation, range(1, 0, 2) is empty => returns 0
        assert add([]) == 0

    def test_large_numbers(self):
        """Large integers should still work correctly."""
        assert add([0, 1000000, 1, 2000000]) == 3000000

    def test_single_odd_index_with_even_value(self):
        """List of length 2: only one odd index."""
        assert add([5, 8]) == 8

    def test_single_odd_index_with_odd_value(self):
        """List of length 2: only one odd index, value is odd."""
        assert add([5, 7]) == 0

    # --- Type and structure verification ---

    def test_returns_integer(self):
        """Result should be an integer."""
        result = add([1, 2, 3, 4])
        assert isinstance(result, int)

    def test_result_is_sum_of_subset(self):
        """Verify the result equals the sum of even elements at odd indices."""
        lst = [10, 3, 5, 8, 2, 7, 9, 12]
        # Odd indices: 1, 3, 5, 7 => values: 3, 8, 7, 12
        # Even among them: 8, 12 => sum = 20
        assert add(lst) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
