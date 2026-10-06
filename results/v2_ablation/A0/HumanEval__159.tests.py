import pytest
from solution import eat


class TestEatFunction:
    """Tests for the eat() function."""

    # ---- Docstring examples ----

    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]

    # ---- Need <= Remaining (enough carrots) ----

    def test_need_equals_remaining(self):
        """When need exactly equals remaining, all needed carrots are available."""
        assert eat(0, 5, 5) == [5, 0]

    def test_need_less_than_remaining(self):
        """When need is less than remaining, full need is satisfied."""
        assert eat(10, 3, 7) == [13, 4]

    def test_need_zero(self):
        """No additional carrots needed; nothing changes."""
        assert eat(5, 0, 10) == [5, 10]

    def test_need_zero_with_no_remaining(self):
        """No carrots needed and none remaining."""
        assert eat(5, 0, 0) == [5, 0]

    def test_number_zero(self):
        """Started with zero eaten carrots."""
        assert eat(0, 3, 5) == [3, 2]

    # ---- Need > Remaining (not enough carrots) ----

    def test_need_greater_than_remaining(self):
        """Eat all remaining carrots but still hungry."""
        assert eat(3, 10, 4) == [7, 0]

    def test_need_much_greater_than_remaining(self):
        """Need far exceeds remaining stock."""
        assert eat(0, 100, 1) == [1, 0]

    def test_need_greater_than_remaining_with_nonzero_number(self):
        """Already eaten some carrots, not enough remaining."""
        assert eat(50, 20, 5) == [55, 0]

    # ---- Edge cases: all zeros ----

    def test_all_zeros(self):
        """All inputs are zero."""
        assert eat(0, 0, 0) == [0, 0]

    # ---- Boundary values (max constraints) ----

    def test_max_values_enough(self):
        """All at maximum constraint with enough stock."""
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_values_not_enough(self):
        """Max number/need but limited remaining."""
        assert eat(1000, 1000, 500) == [1500, 0]

    def test_min_values(self):
        """Minimum non-negative values."""
        assert eat(0, 0, 1) == [0, 1]

    # ---- Return type checks ----

    def test_returns_list(self):
        """Ensure the return value is a list."""
        result = eat(5, 3, 10)
        assert isinstance(result, list)

    def test_returns_two_elements(self):
        """Ensure the returned list has exactly two elements."""
        result = eat(5, 3, 10)
        assert len(result) == 2

    def test_returned_elements_are_integers(self):
        """Ensure both elements of the returned list are integers."""
        result = eat(5, 3, 10)
        assert all(isinstance(x, int) for x in result)

    # ---- Additional logic verification ----

    def test_total_eaten_increases_by_actual_consumed(self):
        """Total eaten should be original + min(need, remaining)."""
        assert eat(7, 15, 8) == [15, 0]  # eats 8, total = 7+8=15

    def test_remaining_decreases_correctly(self):
        """Remaining should decrease by the amount actually consumed."""
        assert eat(0, 5, 20) == [5, 15]  # eats 5, remaining = 20-5=15
