import pytest
from solution import eat


class TestEatNormalCases:
    """Test normal / typical inputs as documented in the docstring examples."""

    def test_example_1(self):
        # need (6) <= remaining (10)
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        # need (8) <= remaining (9)
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        # need (10) == remaining (10), exact match
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        # need (11) > remaining (5), not enough carrots
        assert eat(2, 11, 5) == [7, 0]

    def test_need_less_than_remaining(self):
        # need (3) < remaining (7)
        assert eat(0, 3, 7) == [3, 4]

    def test_need_greater_than_remaining(self):
        # need (20) > remaining (3)
        assert eat(10, 20, 3) == [13, 0]


class TestEatBoundaryCases:
    """Test boundary conditions at the edges of valid input ranges."""

    def test_all_zeros(self):
        # number=0, need=0, remaining=0
        assert eat(0, 0, 0) == [0, 0]

    def test_max_values_equal(self):
        # number=1000, need=1000, remaining=1000
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_number_with_zero_need_and_remaining(self):
        # number=1000, need=0, remaining=0
        assert eat(1000, 0, 0) == [1000, 0]

    def test_need_equals_remaining(self):
        # need exactly equals remaining
        assert eat(5, 5, 5) == [10, 0]

    def test_need_is_zero(self):
        # need=0 means no additional eating required
        assert eat(5, 0, 10) == [5, 10]

    def test_remaining_is_zero_but_need_positive(self):
        # No carrots left; rabbit stays hungry
        assert eat(5, 3, 0) == [5, 0]

    def test_number_is_zero(self):
        # Rabbit hasn't eaten anything yet
        assert eat(0, 5, 10) == [5, 5]

    def test_large_gap_need_vs_remaining(self):
        # need >> remaining
        assert eat(0, 1000, 1) == [1, 0]

    def test_large_gap_remaining_vs_need(self):
        # remaining >> need
        assert eat(0, 1, 1000) == [1, 999]


class TestEatEdgeInputs:
    """Test edge-case inputs including negative numbers and values outside documented constraints."""

    def test_negative_number(self):
        # Function does not validate; arithmetic still works
        assert eat(-1, 5, 10) == [4, 5]

    def test_negative_need(self):
        # need < 0: treated as "no need", so need <= remaining holds
        assert eat(5, -1, 10) == [4, 11]

    def test_negative_remaining(self):
        # remaining < 0: need > remaining, so eats all (negative) remaining
        assert eat(5, 3, -1) == [4, 0]

    def test_all_negative(self):
        # All negatives
        assert eat(-5, -3, -1) == [-8, 2]

    def test_values_beyond_constraints(self):
        # Beyond max constraint of 1000
        assert eat(2000, 2000, 2000) == [4000, 0]

    def test_one_unit_above_need(self):
        # need + 1 == remaining
        assert eat(0, 9, 10) == [9, 1]

    def test_one_unit_below_need(self):
        # need - 1 == remaining
        assert eat(0, 11, 10) == [10, 0]


class TestEatReturnStructure:
    """Verify the return type and structure are always a list of two integers."""

    def test_return_type_normal(self):
        result = eat(5, 6, 10)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_return_type_insufficient_carrots(self):
        result = eat(2, 11, 5)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_first_element_always_total_eaten(self):
        """First element = number + min(need, remaining)."""
        assert eat(7, 3, 5) == [10, 2]   # need <= remaining
        assert eat(7, 8, 5) == [12, 0]   # need > remaining

    def test_second_element_always_leftover(self):
        """Second element = max(0, remaining - need)."""
        assert eat(0, 3, 5) == [3, 2]    # leftover = 5 - 3 = 2
        assert eat(0, 7, 5) == [5, 0]    # leftover = 0
