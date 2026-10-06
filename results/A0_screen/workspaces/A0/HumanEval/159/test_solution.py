import pytest
from solution import eat


class TestEatFunction:
    """Tests for the eat() function."""

    # ── Docstring examples ──────────────────────────────────────────────

    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]

    # ── Enough remaining carrots ────────────────────────────────────────

    def test_need_equals_remaining(self):
        """When need == remaining, all remaining carrots are eaten."""
        assert eat(0, 5, 5) == [5, 0]

    def test_need_less_than_remaining(self):
        """When need < remaining, rabbit eats exactly what it needs."""
        assert eat(10, 3, 7) == [13, 4]

    def test_need_greater_than_remaining(self):
        """When need > remaining, rabbit eats all remaining carrots."""
        assert eat(10, 15, 7) == [17, 0]

    # ── Zero edge cases ─────────────────────────────────────────────────

    def test_all_zeros(self):
        assert eat(0, 0, 0) == [0, 0]

    def test_zero_need(self):
        """Rabbit doesn't need any more carrots."""
        assert eat(5, 0, 10) == [5, 10]

    def test_zero_number(self):
        """Rabbit hasn't eaten anything yet."""
        assert eat(0, 3, 5) == [3, 2]

    def test_zero_remaining(self):
        """No carrots left in stock."""
        assert eat(5, 3, 0) == [5, 0]

    # ── Large values ────────────────────────────────────────────────────

    def test_max_values(self):
        """Test with maximum constraint values (1000)."""
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_large_need_exceeds_remaining(self):
        """Large need that exceeds remaining."""
        assert eat(500, 1000, 200) == [700, 0]

    def test_large_need_within_remaining(self):
        """Large need that is within remaining."""
        assert eat(500, 200, 1000) == [700, 800]

    # ── Return type checks ──────────────────────────────────────────────

    def test_returns_list(self):
        result = eat(5, 6, 10)
        assert isinstance(result, list)

    def test_returns_two_elements(self):
        result = eat(5, 6, 10)
        assert len(result) == 2

    def test_returns_integers(self):
        result = eat(5, 6, 10)
        assert all(isinstance(x, int) for x in result)

    # ── Invariant / property-based checks ───────────────────────────────

    def test_total_consumed_plus_remaining_equals_stock_plus_initial(self):
        """
        Property: number + need_used + remaining_after == number + original_remaining
        i.e., total eaten + leftover = initial eaten + initial stock.
        """
        for number, need, remaining in [
            (5, 6, 10), (4, 8, 9), (1, 10, 10), (2, 11, 5),
            (0, 0, 0), (100, 50, 200), (100, 300, 200),
        ]:
            total_eaten, leftovers = eat(number, need, remaining)
            assert total_eaten + leftovers == number + remaining

    def test_leftovers_never_negative(self):
        """Remaining carrots should never be negative."""
        for number, need, remaining in [
            (i, j, k) for i in range(0, 11)
            for j in range(0, 11)
            for k in range(0, 11)
        ]:
            _, leftovers = eat(number, need, remaining)
            assert leftovers >= 0

    def test_total_eaten_does_not_exceed_number_plus_remaining(self):
        """Total eaten cannot exceed what was available."""
        for number, need, remaining in [
            (i, j, k) for i in range(0, 11)
            for j in range(0, 11)
            for k in range(0, 11)
        ]:
            total_eaten, _ = eat(number, need, remaining)
            assert total_eaten <= number + remaining

    def test_when_enough_carrots_total_eaten_equals_number_plus_need(self):
        """If remaining >= need, total eaten should be number + need."""
        for number in range(0, 11):
            for need in range(0, 11):
                for remaining in range(need, 11):
                    total_eaten, _ = eat(number, need, remaining)
                    assert total_eaten == number + need

    def test_when_not_enough_carrots_total_eaten_equals_number_plus_remaining(self):
        """If remaining < need, total eaten should be number + remaining."""
        for number in range(0, 11):
            for need in range(0, 11):
                for remaining in range(0, min(need, 11)):
                    total_eaten, _ = eat(number, need, remaining)
                    assert total_eaten == number + remaining
