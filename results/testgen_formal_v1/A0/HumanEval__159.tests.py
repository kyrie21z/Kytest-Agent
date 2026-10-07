import pytest
from solution import eat


class TestEatFunction:
    """Tests for the eat() function."""

    # --- Examples from docstring ---

    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]

    # --- Enough remaining carrots (need <= remaining) ---

    def test_need_equals_remaining(self):
        """When need exactly equals remaining, all needed carrots are eaten."""
        assert eat(0, 5, 5) == [5, 0]

    def test_need_less_than_remaining(self):
        """When need is less than remaining, only 'need' carrots are eaten."""
        assert eat(10, 3, 7) == [13, 4]

    def test_need_zero(self):
        """When need is zero, no additional carrots are eaten."""
        assert eat(5, 0, 10) == [5, 10]

    def test_need_zero_with_no_remaining(self):
        """When need is zero and remaining is also zero."""
        assert eat(5, 0, 0) == [5, 0]

    def test_all_zeros(self):
        """All inputs are zero."""
        assert eat(0, 0, 0) == [0, 0]

    # --- Not enough remaining carrots (need > remaining) ---

    def test_need_greater_than_remaining(self):
        """When need exceeds remaining, all remaining are eaten."""
        assert eat(3, 10, 4) == [7, 0]

    def test_need_much_greater_than_remaining(self):
        """Need far exceeds remaining; still eat all remaining."""
        assert eat(0, 100, 1) == [1, 0]

    def test_need_greater_than_remaining_with_existing_eaten(self):
        """Existing eaten count is added even when not enough remaining."""
        assert eat(50, 20, 5) == [55, 0]

    # --- Boundary / edge cases ---

    def test_max_values_enough_remaining(self):
        """Maximum values where need <= remaining."""
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_values_not_enough_remaining(self):
        """Maximum values where need > remaining."""
        assert eat(1000, 1000, 500) == [1500, 0]

    def test_large_number_small_need(self):
        """Large number of already eaten carrots with small need."""
        assert eat(1000, 1, 1000) == [1001, 999]

    def test_large_remaining_small_need(self):
        """Small need against large remaining stock."""
        assert eat(0, 1, 1000) == [1, 999]

    def test_return_type_is_list(self):
        """Ensure the return type is always a list."""
        result = eat(5, 6, 10)
        assert isinstance(result, list)

    def test_return_length_is_two(self):
        """Ensure the returned list always has exactly two elements."""
        result = eat(5, 6, 10)
        assert len(result) == 2

    def test_return_elements_are_integers(self):
        """Ensure both elements in the returned list are integers."""
        result = eat(5, 6, 10)
        assert isinstance(result[0], int)
        assert isinstance(result[1], int)

    # --- Additional logical checks ---

    def test_total_eaten_includes_original(self):
        """Total eaten should be original 'number' plus what was actually consumed."""
        # When enough remaining
        result = eat(5, 6, 10)
        assert result[0] == 5 + 6  # total eaten
        assert result[1] == 10 - 6  # remaining left

    def test_total_eaten_when_insufficient(self):
        """Total eaten should be original 'number' plus all remaining carrots."""
        result = eat(2, 11, 5)
        assert result[0] == 2 + 5  # total eaten
        assert result[1] == 0  # nothing left
