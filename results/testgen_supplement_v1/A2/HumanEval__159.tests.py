"""Unit tests for solution.eat().

The eat(number, need, remaining) function returns [total_eaten, left_over]:
  - If need <= remaining:  [number + need, remaining - need]
  - If need > remaining:   [number + remaining, 0]

Constraints documented: 0 <= number, need, remaining <= 1000
"""

import pytest
from solution import eat


# ---------------------------------------------------------------------------
# 1. Normal cases – directly from the docstring examples
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    def test_example_1(self):
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        assert eat(2, 11, 5) == [7, 0]


# ---------------------------------------------------------------------------
# 2. Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries defined by the constraint 0 <= x <= 1000."""

    def test_all_zeros(self):
        """Every argument is zero – the smallest valid input."""
        assert eat(0, 0, 0) == [0, 0]

    def test_max_values(self):
        """Every argument is at the upper bound of the constraint."""
        assert eat(1000, 1000, 1000) == [2000, 0]

    def test_need_equals_remaining(self):
        """Exact boundary between the two branches (need == remaining)."""
        assert eat(3, 5, 5) == [8, 0]

    def test_need_is_zero_with_stock(self):
        """Rabbit needs nothing; all stock remains untouched."""
        assert eat(5, 0, 10) == [5, 10]

    def test_remaining_is_zero_but_need_positive(self):
        """No stock available; rabbit eats nothing and stays hungry."""
        assert eat(5, 10, 0) == [5, 0]

    def test_number_is_zero(self):
        """Rabbit hasn't eaten anything yet."""
        assert eat(0, 5, 10) == [5, 5]

    def test_number_at_max_with_small_need_and_stock(self):
        """number at max, need and remaining small."""
        assert eat(1000, 1, 1) == [1001, 0]

    def test_need_at_max_with_large_remaining(self):
        """need at max, remaining exceeds need."""
        assert eat(0, 1000, 1000) == [1000, 0]

    def test_remaining_at_max_with_small_need(self):
        """remaining at max, need is small."""
        assert eat(0, 1, 1000) == [1, 999]


# ---------------------------------------------------------------------------
# 3. Empty / zero-size inputs (covered above, but grouped here for clarity)
# ---------------------------------------------------------------------------

class TestZeroInputs:
    def test_all_arguments_zero(self):
        assert eat(0, 0, 0) == [0, 0]

    def test_only_number_nonzero(self):
        assert eat(7, 0, 0) == [7, 0]

    def test_only_need_nonzero(self):
        # need=3 > remaining=0 → else branch: [0+0, 0] = [0, 0]
        assert eat(0, 3, 0) == [0, 0]

    def test_only_remaining_nonzero(self):
        assert eat(0, 0, 3) == [0, 3]


# ---------------------------------------------------------------------------
# 4. Invalid inputs – outside documented constraints
# The function does NOT validate inputs, so it still computes.
# We test that behaviour rather than expecting an exception.
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    def test_negative_number(self):
        assert eat(-1, 5, 10) == [4, 5]

    def test_negative_need(self):
        assert eat(5, -3, 10) == [2, 13]

    def test_negative_remaining(self):
        # need=3 > remaining=-1 → else branch: [5+(-1), 0] = [4, 0]
        assert eat(5, 3, -1) == [4, 0]

    def test_all_negative(self):
        # need=-2 > remaining=-3 → else branch: [-1+(-3), 0] = [-4, 0]
        assert eat(-1, -2, -3) == [-4, 0]

    def test_values_exceeding_upper_constraint(self):
        """Values > 1000 are not rejected by the function."""
        assert eat(2000, 3000, 4000) == [5000, 1000]

    def test_mixed_valid_and_invalid(self):
        assert eat(500, 1500, 800) == [1300, 0]


# ---------------------------------------------------------------------------
# 5. Additional logic coverage – ensure both branches are well tested
# ---------------------------------------------------------------------------

class TestBranchCoverage:
    """Extra cases to guarantee both conditional branches are exercised."""

    # --- Branch: need <= remaining ---
    def test_sufficient_stock_one_carrot(self):
        assert eat(0, 1, 1) == [1, 0]

    def test_sufficient_stock_large_gap(self):
        assert eat(100, 1, 1000) == [101, 999]

    def test_sufficient_stock_equal(self):
        assert eat(50, 50, 50) == [100, 0]

    # --- Branch: need > remaining ---
    def test_insufficient_stock_by_one(self):
        assert eat(0, 5, 4) == [4, 0]

    def test_insufficient_stock_large_gap(self):
        assert eat(0, 100, 1) == [1, 0]

    def test_insufficient_stock_extreme(self):
        assert eat(0, 1000, 0) == [0, 0]


# ---------------------------------------------------------------------------
# 6. Return type checks
# ---------------------------------------------------------------------------

class TestReturnType:
    def test_returns_list(self):
        result = eat(0, 0, 0)
        assert isinstance(result, list)

    def test_returns_two_elements(self):
        result = eat(0, 0, 0)
        assert len(result) == 2

    def test_elements_are_integers(self):
        result = eat(5, 6, 10)
        assert all(isinstance(x, int) for x in result)
