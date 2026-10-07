"""Unit tests for solution.eat().

The eat(number, need, remaining) function simulates a hungry rabbit eating carrots.
It returns [total_eaten, left] where:
  - total_eaten = number + min(need, remaining)
  - left        = max(0, remaining - need)

Documented constraints:
  * 0 <= number <= 1000
  * 0 <= need   <= 1000
  * 0 <= remaining <= 1000
"""

import pytest
from solution import eat


# ---------------------------------------------------------------------------
# 1. Normal / canonical cases (from the docstring examples)
# ---------------------------------------------------------------------------

class TestNormalCases:
    def test_example_1(self):
        """need < remaining: rabbit eats all that it needs."""
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        """need < remaining: another typical case."""
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        """need == remaining: rabbit eats everything it needs and stock hits 0."""
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        """need > remaining: rabbit eats all remaining carrots but is still hungry."""
        assert eat(2, 11, 5) == [7, 0]


# ---------------------------------------------------------------------------
# 2. Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    def test_all_zeros(self):
        """All parameters are zero — nothing to eat, nothing left."""
        assert eat(0, 0, 0) == [0, 0]

    def test_max_values_need_equals_remaining(self):
        """Max values where need == remaining."""
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_max_values_need_greater_than_remaining(self):
        """Max number, max need, minimal remaining."""
        assert eat(1000, 1000, 0) == [1000, 0]

    def test_min_number_with_need_greater_than_remaining(self):
        """Smallest number, need exceeds remaining."""
        assert eat(0, 1000, 500) == [500, 0]

    def test_min_number_with_need_less_than_remaining(self):
        """Smallest number, need well within remaining."""
        assert eat(0, 1, 1000) == [1, 999]

    def test_need_is_zero(self):
        """Rabbit needs nothing; stock unchanged."""
        assert eat(5, 0, 10) == [5, 10]

    def test_remaining_is_zero_with_need_positive(self):
        """No carrots left; rabbit eats nothing more."""
        assert eat(5, 3, 0) == [5, 0]

    def test_remaining_is_zero_with_need_zero(self):
        """No carrots left and rabbit needs nothing."""
        assert eat(5, 0, 0) == [5, 0]

    def test_large_number_small_need(self):
        """Large base eaten, small additional need."""
        assert eat(999, 1, 500) == [1000, 499]

    def test_large_number_large_need_exceeds_remaining(self):
        """Large base eaten, large need exceeding remaining."""
        assert eat(999, 500, 200) == [1199, 0]


# ---------------------------------------------------------------------------
# 3. Edge cases with zero-size / empty-like inputs
# ---------------------------------------------------------------------------

class TestZeroSizeInputs:
    def test_number_zero_need_zero_remaining_nonzero(self):
        """Already eaten nothing, need nothing, but stock exists."""
        assert eat(0, 0, 100) == [0, 100]

    def test_number_nonzero_need_zero_remaining_zero(self):
        """Ate some, need nothing, nothing left."""
        assert eat(10, 0, 0) == [10, 0]

    def test_number_zero_need_nonzero_remaining_zero(self):
        """Haven't eaten yet, need carrots, none available."""
        assert eat(0, 5, 0) == [0, 0]


# ---------------------------------------------------------------------------
# 4. Invalid inputs outside documented constraints
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """The function does not validate inputs, so we verify its raw behaviour."""

    def test_negative_number(self):
        """Negative 'number' — function still computes arithmetically."""
        assert eat(-1, 5, 10) == [4, 5]

    def test_negative_need(self):
        """Negative 'need' — function treats it as needing negative carrots.
        
        With need=-3, remaining=10: need <= remaining is True,
        so returns [number + need, remaining - need] = [5 + (-3), 10 - (-3)] = [2, 13].
        """
        assert eat(5, -3, 10) == [2, 13]

    def test_negative_remaining(self):
        """Negative 'remaining' — stock is negative; need > remaining triggers else branch."""
        assert eat(5, 3, -1) == [4, 0]

    def test_number_exceeds_constraint(self):
        """number > 1000 — function still works."""
        assert eat(2000, 10, 10) == [2010, 0]

    def test_need_exceeds_constraint(self):
        """need > 1000 — function still works."""
        assert eat(5, 2000, 10) == [15, 0]

    def test_remaining_exceeds_constraint(self):
        """remaining > 1000 — function still works."""
        assert eat(5, 10, 2000) == [15, 1990]


# ---------------------------------------------------------------------------
# 5. Exception cases — non-numeric / unexpected types
# ---------------------------------------------------------------------------

class TestExceptionCases:
    def test_string_number_raises_typeerror(self):
        """Passing a string for 'number' causes TypeError in arithmetic."""
        with pytest.raises(TypeError):
            eat("5", 10, 10)

    def test_string_need_raises_typeerror(self):
        """Passing a string for 'need' causes TypeError."""
        with pytest.raises(TypeError):
            eat(5, "10", 10)

    def test_string_remaining_raises_typeerror(self):
        """Passing a string for 'remaining' causes TypeError."""
        with pytest.raises(TypeError):
            eat(5, 10, "10")

    def test_none_input_raises_typeerror(self):
        """Passing None for any argument causes TypeError."""
        with pytest.raises(TypeError):
            eat(None, 10, 10)

    def test_list_input_raises_typeerror(self):
        """Passing a list instead of an int causes TypeError."""
        with pytest.raises(TypeError):
            eat([5], 10, 10)
