import pytest
from solution import eat


class TestEatNormalCases:
    """Test cases from the docstring examples."""

    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]


class TestEatBoundaryCases:
    """Boundary cases at the edges of valid input ranges (0 to 1000)."""

    def test_all_zeros(self):
        # No carrots eaten, none needed, none remaining
        assert eat(0, 0, 0) == [0, 0]

    def test_max_values_need_equals_remaining(self):
        # Max values, need exactly equals remaining
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_number_no_need(self):
        # Already ate max, don't need more
        assert eat(1000, 0, 1000) == [1000, 1000]

    def test_max_need_no_remaining(self):
        # Need max carrots but nothing left
        assert eat(0, 1000, 0) == [0, 0]

    def test_need_exceeds_remaining_by_one(self):
        # Need is just one more than remaining
        assert eat(5, 11, 10) == [15, 0]

    def test_need_is_one_less_than_remaining(self):
        # Need is just one less than remaining
        assert eat(5, 9, 10) == [14, 1]

    def test_minimal_nonzero_case(self):
        # Minimal positive values
        assert eat(1, 1, 1) == [2, 0]

    def test_large_number_small_need(self):
        # Large already eaten, small need
        assert eat(999, 1, 5) == [1000, 4]

    def test_small_number_large_need(self):
        # Small already eaten, large need exceeding remaining
        assert eat(1, 500, 100) == [501, 0]

    def test_equal_all_three(self):
        # All three parameters equal and nonzero
        assert eat(7, 7, 7) == [14, 0]


class TestEatZeroSizeInputs:
    """Cases involving zero-sized inputs."""

    def test_zero_need_with_positive_remaining(self):
        # Don't need to eat anything, carrots remain untouched
        assert eat(3, 0, 5) == [3, 5]

    def test_zero_remaining_with_positive_need(self):
        # Need carrots but stock is empty
        assert eat(3, 5, 0) == [3, 0]

    def test_zero_number_with_positive_need_and_remaining(self):
        # Haven't eaten any yet, need and have remaining
        assert eat(0, 5, 10) == [5, 5]

    def test_zero_number_zero_need_positive_remaining(self):
        assert eat(0, 0, 100) == [0, 100]

    def test_zero_number_positive_need_zero_remaining(self):
        assert eat(0, 50, 0) == [0, 0]


class TestEatInvalidInputs:
    """Test behavior with inputs outside documented constraints."""

    def test_negative_number(self):
        # Negative 'number' — function performs arithmetic regardless
        assert eat(-1, 5, 10) == [4, 5]

    def test_negative_need(self):
        # Negative 'need' — treated as needing fewer than 0 carrots
        assert eat(5, -3, 10) == [2, 13]

    def test_negative_remaining(self):
        # Negative 'remaining' — function still computes
        assert eat(5, 3, -1) == [4, 0]

    def test_values_exceeding_max_constraint(self):
        # Values above the documented upper bound of 1000
        assert eat(2000, 3000, 4000) == [5000, 1000]

    def test_mixed_negative_and_large(self):
        assert eat(-100, 5000, 200) == [-800, 0]


class TestEatEdgeConditionNeedEqualsRemaining:
    """Specifically test when need == remaining (boundary between two branches)."""

    def test_need_equals_remaining_various_numbers(self):
        assert eat(0, 5, 5) == [5, 0]
        assert eat(10, 5, 5) == [15, 0]
        assert eat(100, 100, 100) == [200, 0]

    def test_need_greater_than_remaining(self):
        assert eat(0, 6, 5) == [5, 0]
        assert eat(10, 20, 5) == [15, 0]

    def test_need_less_than_remaining(self):
        assert eat(0, 4, 5) == [4, 1]
        assert eat(10, 3, 5) == [13, 2]


class TestEatReturnStructure:
    """Verify the return value is always a list of two integers."""

    def test_return_type_and_length(self):
        result = eat(5, 6, 10)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_total_eaten_at_least_number(self):
        # Total eaten should always be >= number (can't un-eat)
        for number in range(0, 1001):
            for need in range(0, 1001):
                for remaining in range(0, 1001):
                    total, left = eat(number, need, remaining)
                    assert total >= number, \
                        f"eat({number}, {need}, {remaining}) gave total {total} < {number}"

    def test_left_never_negative(self):
        # Leftover should never be negative
        for number in range(0, 1001):
            for need in range(0, 1001):
                for remaining in range(0, 1001):
                    total, left = eat(number, need, remaining)
                    assert left >= 0, \
                        f"eat({number}, {need}, {remaining}) gave left {left} < 0"

    def test_invariant_total_plus_left_equals_number_plus_consumed(self):
        # total_eaten + left_over = number + min(need, remaining)
        for number in range(0, 1001):
            for need in range(0, 1001):
                for remaining in range(0, 1001):
                    total, left = eat(number, need, remaining)
                    consumed = min(need, remaining)
                    assert total + left == number + consumed, \
                        f"eat({number}, {need}, {remaining}): " \
                        f"{total} + {left} != {number} + {consumed}"
