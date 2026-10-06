import pytest
from solution import eat


class TestEatDocstringExamples:
    """Test cases directly from the function's docstring."""

    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]


class TestEatNormalCases:
    """Typical inputs where need < remaining (enough carrots available)."""

    def test_need_less_than_remaining(self):
        assert eat(10, 3, 7) == [13, 4]

    def test_need_much_less_than_remaining(self):
        assert eat(100, 1, 50) == [101, 49]

    def test_need_one_less_than_remaining(self):
        assert eat(0, 4, 5) == [4, 1]


class TestEatBoundaryCases:
    """Boundary conditions at edges of valid input ranges (0 to 1000)."""

    def test_all_zeros(self):
        assert eat(0, 0, 0) == [0, 0]

    def test_max_values_equal(self):
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_number_and_remaining_zero_need(self):
        assert eat(1000, 0, 1000) == [1000, 1000]

    def test_max_need_no_remaining(self):
        assert eat(0, 1000, 0) == [0, 0]

    def test_max_number_zero_need_zero_remaining(self):
        assert eat(1000, 0, 0) == [1000, 0]

    def test_need_equals_remaining(self):
        """Exact boundary: need == remaining, eats all needed, zero left."""
        assert eat(5, 5, 5) == [10, 0]

    def test_need_exceeds_remaining_by_one(self):
        """Just over the boundary: need == remaining + 1."""
        assert eat(5, 6, 5) == [10, 0]

    def test_need_below_remaining_by_one(self):
        """Just under the boundary: need == remaining - 1."""
        assert eat(5, 4, 5) == [9, 1]


class TestEatZeroInputs:
    """Cases involving zero for one or more parameters."""

    def test_zero_need(self):
        assert eat(7, 0, 10) == [7, 10]

    def test_zero_remaining(self):
        assert eat(7, 5, 0) == [7, 0]

    def test_zero_number(self):
        assert eat(0, 3, 5) == [3, 2]

    def test_zero_number_and_zero_need(self):
        assert eat(0, 0, 5) == [0, 5]

    def test_zero_number_and_zero_remaining(self):
        assert eat(0, 5, 0) == [0, 0]


class TestEatNotEnoughCarrots:
    """Cases where remaining < need (not enough carrots in stock)."""

    def test_not_enough_carrots(self):
        assert eat(3, 10, 4) == [7, 0]

    def test_remaining_is_half_of_need(self):
        assert eat(0, 10, 5) == [5, 0]

    def test_remaining_is_one(self):
        assert eat(0, 100, 1) == [1, 0]

    def test_remaining_is_zero(self):
        assert eat(50, 20, 0) == [50, 0]


class TestEatReturnTypesAndStructure:
    """Verify return type and structure."""

    def test_returns_list(self):
        result = eat(5, 6, 10)
        assert isinstance(result, list)

    def test_returns_two_elements(self):
        result = eat(5, 6, 10)
        assert len(result) == 2

    def test_returns_integers(self):
        result = eat(5, 6, 10)
        assert all(isinstance(x, int) for x in result)

    def test_first_element_is_total_eaten(self):
        """Total eaten should always be >= number (original eaten amount)."""
        for number, need, remaining in [(5, 6, 10), (4, 8, 9), (1, 10, 10), (2, 11, 5)]:
            result = eat(number, need, remaining)
            assert result[0] >= number

    def test_second_element_never_negative(self):
        """Carrots left should never be negative."""
        for number, need, remaining in [(5, 6, 10), (4, 8, 9), (1, 10, 10), (2, 11, 5)]:
            result = eat(number, need, remaining)
            assert result[1] >= 0

    def test_sum_matches_available(self):
        """number + min(need, remaining) should equal total eaten."""
        for number, need, remaining in [(5, 6, 10), (4, 8, 9), (1, 10, 10), (2, 11, 5)]:
            result = eat(number, need, remaining)
            actual_eaten = result[0] - number
            expected_eaten = min(need, remaining)
            assert actual_eaten == expected_eaten
