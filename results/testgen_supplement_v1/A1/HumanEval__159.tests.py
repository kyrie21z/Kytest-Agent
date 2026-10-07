"""Unit tests for solution.eat().

The eat(number, need, remaining) function models a hungry rabbit eating carrots:
  - If need <= remaining: return [number + need, remaining - need]
  - If need > remaining:  return [number + remaining, 0]

Constraints documented in the docstring:
  * 0 <= number <= 1000
  * 0 <= need <= 1000
  * 0 <= remaining <= 1000
"""

import pytest
from solution import eat


# ──────────────────────────────────────────────
# 1. Normal / typical cases (from docstring examples)
# ──────────────────────────────────────────────

class TestDocstringExamples:
    """Cases explicitly given in the function's docstring."""

    def test_example_1(self):
        # eat(5, 6, 10) -> [11, 4]
        assert eat(5, 6, 10) == [11, 4]

    def test_example_2(self):
        # eat(4, 8, 9) -> [12, 1]
        assert eat(4, 8, 9) == [12, 1]

    def test_example_3(self):
        # eat(1, 10, 10) -> [11, 0]
        assert eat(1, 10, 10) == [11, 0]

    def test_example_4(self):
        # eat(2, 11, 5) -> [7, 0]
        assert eat(2, 11, 5) == [7, 0]


# ──────────────────────────────────────────────
# 2. Boundary cases at edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryNeedEqualsRemaining:
    """When need exactly equals remaining, all remaining are eaten."""

    def test_all_zeros(self):
        assert eat(0, 0, 0) == [0, 0]

    def test_need_equals_remaining_nonzero(self):
        assert eat(5, 5, 5) == [10, 0]

    def test_max_values_equal(self):
        assert eat(1000, 1000, 1000) == [2000, 0]


class TestBoundaryNeedGreaterThanRemaining:
    """Not enough carrots; rabbit eats everything available."""

    def test_no_remaining_carrots(self):
        assert eat(5, 3, 0) == [5, 0]

    def test_need_exceeds_remaining(self):
        assert eat(0, 100, 0) == [0, 0]

    def test_need_much_larger_than_remaining(self):
        assert eat(100, 50, 10) == [110, 0]

    def test_max_number_with_insufficient_remaining(self):
        assert eat(1000, 1000, 1) == [1001, 0]


class TestBoundaryNeedLessThanRemaining:
    """Enough carrots; rabbit eats what it needs."""

    def test_need_zero_enough_remaining(self):
        assert eat(5, 0, 10) == [5, 10]

    def test_need_zero_no_remaining(self):
        assert eat(5, 0, 0) == [5, 0]

    def test_small_need_large_remaining(self):
        assert eat(50, 10, 100) == [60, 90]

    def test_max_number_sufficient_remaining(self):
        assert eat(1000, 0, 1000) == [1000, 1000]


class TestBoundaryMinNumber:
    """Rabbit has eaten zero carrots so far."""

    def test_zero_number_need_less_remaining(self):
        assert eat(0, 3, 10) == [3, 7]

    def test_zero_number_need_greater_remaining(self):
        assert eat(0, 10, 3) == [3, 0]

    def test_zero_number_need_equals_remaining(self):
        assert eat(0, 7, 7) == [7, 0]


# ──────────────────────────────────────────────
# 3. Empty / null / zero-size inputs
# ──────────────────────────────────────────────

class TestZeroInputs:
    """Edge cases where one or more arguments are zero."""

    def test_all_zero(self):
        assert eat(0, 0, 0) == [0, 0]

    def test_only_number_nonzero(self):
        assert eat(42, 0, 0) == [42, 0]

    def test_only_need_nonzero(self):
        # eat(0, 42, 0): need=42 > remaining=0 → else branch
        # returns [number + remaining, 0] = [0 + 0, 0] = [0, 0]
        assert eat(0, 42, 0) == [0, 0]

    def test_only_remaining_nonzero(self):
        assert eat(0, 0, 42) == [0, 42]


# ──────────────────────────────────────────────
# 4. Invalid inputs (outside documented constraints)
# ──────────────────────────────────────────────

class TestNegativeInputs:
    """Inputs below the documented minimum of 0.
    The function does not validate constraints, so these
    should still produce deterministic results based on logic."""

    def test_negative_number(self):
        assert eat(-1, 5, 10) == [4, 5]

    def test_negative_need(self):
        assert eat(5, -3, 10) == [2, 13]

    def test_negative_remaining(self):
        assert eat(5, 3, -1) == [4, 0]

    def test_all_negative(self):
        # eat(-1, -2, -3): need=-2 > remaining=-3 → else branch
        # returns [number + remaining, 0] = [-1 + (-3), 0] = [-4, 0]
        assert eat(-1, -2, -3) == [-4, 0]


class TestLargeInputsBeyondConstraint:
    """Values exceeding the documented upper bound of 1000."""

    def test_large_number(self):
        assert eat(2000, 100, 500) == [2100, 400]

    def test_large_need(self):
        assert eat(100, 2000, 500) == [600, 0]

    def test_large_remaining(self):
        assert eat(100, 50, 2000) == [150, 1950]


# ──────────────────────────────────────────────
# 5. Exception cases – invalid argument types
# ──────────────────────────────────────────────

class TestInvalidTypes:
    """Passing non-integer types. The function performs arithmetic
    comparisons/additions, so some types may work while others fail."""

    @pytest.mark.parametrize("args", [
        {"number": "5", "need": 6, "remaining": 10},
        {"number": 5, "need": "6", "remaining": 10},
        {"number": 5, "need": 6, "remaining": "10"},
        {"number": None, "need": 6, "remaining": 10},
        {"number": 5, "need": None, "remaining": 10},
        {"number": 5, "need": 6, "remaining": None},
        {"number": [], "need": 6, "remaining": 10},
        {"number": 5, "need": {}, "remaining": 10},
    ])
    def test_raises_type_error(self, args):
        """Non-numeric types should raise TypeError (or similar)."""
        with pytest.raises(TypeError):
            eat(**args)

    def test_float_inputs(self):
        """Floats are technically numeric but outside integer constraint."""
        # Python allows float arithmetic, so no exception is raised.
        # We document the actual behaviour rather than asserting error.
        result = eat(5.5, 6.0, 10.5)
        assert result == [11.5, 4.5]


# ──────────────────────────────────────────────
# 6. Return-value shape & type checks
# ──────────────────────────────────────────────

class TestReturnValueShape:
    """Ensure the function always returns a list of two elements."""

    @pytest.mark.parametrize("number, need, remaining, expected", [
        (0, 0, 0, [0, 0]),
        (5, 6, 10, [11, 4]),
        (2, 11, 5, [7, 0]),
        (1000, 1000, 1000, [2000, 0]),
    ])
    def test_returns_list_of_two_elements(self, number, need, remaining, expected):
        result = eat(number, need, remaining)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result == expected
