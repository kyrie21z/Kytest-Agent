"""Unit tests for prod_signs in solution.py.

Function behavior (from docstring and code):
- Input: list of integers `arr`.
- Returns None if arr is empty.
- Returns 0 if any element is 0 (sign product becomes 0).
- Otherwise returns (sum of absolute values) * (product of signs),
  where sign(x) = 1 if x > 0, -1 if x < 0.
"""

import pytest
from solution import prod_signs


# ---------------------------------------------------------------------------
# Normal / typical cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical non-trivial inputs."""

    def test_all_positive(self):
        # [1, 2, 3] → sum_abs=6, sign_prod=1 → 6
        assert prod_signs([1, 2, 3]) == 6

    def test_all_negative(self):
        # [-1, -2, -3] → sum_abs=6, sign_prod=(-1)^3=-1 → -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_mixed_even_negatives(self):
        # [1, -2, -3] → sum_abs=6, sign_prod=1 → 6
        assert prod_signs([1, -2, -3]) == 6

    def test_mixed_odd_negatives(self):
        # [1, 2, 2, -4] → sum_abs=9, sign_prod=-1 → -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_single_positive(self):
        # [5] → sum_abs=5, sign_prod=1 → 5
        assert prod_signs([5]) == 5

    def test_single_negative(self):
        # [-7] → sum_abs=7, sign_prod=-1 → -7
        assert prod_signs([-7]) == -7

    def test_with_zero(self):
        # [0, 1] → contains 0 → 0
        assert prod_signs([0, 1]) == 0

    def test_zero_alone(self):
        # [0] → contains 0 → 0
        assert prod_signs([0]) == 0

    def test_multiple_zeros(self):
        # [0, 0, 0] → contains 0 → 0
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_among_positives(self):
        # [1, 0, 2] → contains 0 → 0
        assert prod_signs([1, 0, 2]) == 0

    def test_zero_among_negatives(self):
        # [-1, 0, -2] → contains 0 → 0
        assert prod_signs([-1, 0, -2]) == 0

    def test_large_values(self):
        # [100, 200, -300] → sum_abs=600, sign_prod=-1 → -600
        assert prod_signs([100, 200, -300]) == -600

    def test_many_elements(self):
        # [1]*100 → sum_abs=100, sign_prod=1 → 100
        assert prod_signs([1] * 100) == 100

    def test_alternating_ones(self):
        # [1, -1, 1, -1] → sum_abs=4, sign_prod=1 → 4
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_alternating_ones_odd_count(self):
        # [1, -1, 1] → sum_abs=3, sign_prod=-1 → -3
        assert prod_signs([1, -1, 1]) == -3


# ---------------------------------------------------------------------------
# Boundary cases at edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of valid integer inputs."""

    def test_largest_negative_single(self):
        # [-1] → sum_abs=1, sign_prod=-1 → -1
        assert prod_signs([-1]) == -1

    def test_largest_positive_single(self):
        # [1] → sum_abs=1, sign_prod=1 → 1
        assert prod_signs([1]) == 1

    def test_two_zeros(self):
        # [0, 0] → contains 0 → 0
        assert prod_signs([0, 0]) == 0

    def test_one_element_zero(self):
        # [0] → contains 0 → 0
        assert prod_signs([0]) == 0

    def test_two_elements_both_positive(self):
        # [1, 1] → sum_abs=2, sign_prod=1 → 2
        assert prod_signs([1, 1]) == 2

    def test_two_elements_both_negative(self):
        # [-1, -1] → sum_abs=2, sign_prod=1 → 2
        assert prod_signs([-1, -1]) == 2

    def test_two_elements_mixed(self):
        # [1, -1] → sum_abs=2, sign_prod=-1 → -2
        assert prod_signs([1, -1]) == -2

    def test_three_elements_all_same_sign(self):
        # [2, 2, 2] → sum_abs=6, sign_prod=1 → 6
        assert prod_signs([2, 2, 2]) == 6

    def test_three_elements_one_different_sign(self):
        # [-2, 2, 2] → sum_abs=6, sign_prod=-1 → -6
        assert prod_signs([-2, 2, 2]) == -6


# ---------------------------------------------------------------------------
# Empty, null, or zero-size inputs
# ---------------------------------------------------------------------------

class TestEmptyInputs:
    """Tests for empty or edge-case inputs."""

    def test_empty_list(self):
        # [] → None (documented)
        assert prod_signs([]) is None

    def test_empty_list_identity_check(self):
        # Ensure it returns None (not just falsy)
        result = prod_signs([])
        assert result is None


# ---------------------------------------------------------------------------
# Invalid inputs — function does not document handling; expect exceptions
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests for inputs outside the documented contract."""

    def test_none_input_raises_type_error(self):
        # Passing None is not a valid list; should raise TypeError
        with pytest.raises(TypeError):
            prod_signs(None)

    def test_string_input_raises_type_error(self):
        # Passing a string is not a valid list; should raise TypeError
        with pytest.raises(TypeError):
            prod_signs("hello")

    def test_integer_input_raises_type_error(self):
        # Passing an int is not a valid list; should raise TypeError
        with pytest.raises(TypeError):
            prod_signs(42)

    def test_tuple_input(self):
        # A tuple behaves like a sequence; the function iterates over it.
        # (1, -2) → sum_abs=3, sign_prod=-1 → -3
        assert prod_signs((1, -2)) == -3


# ---------------------------------------------------------------------------
# Exception cases — verify specific error conditions
# ---------------------------------------------------------------------------

class TestExceptionCases:
    """Tests where the function raises exceptions on invalid usage."""

    def test_non_iterable_raises(self):
        # dict is iterable but iterating gives keys, not values as expected.
        # This is technically "works" but let's confirm it doesn't crash silently.
        # Actually, iterating a dict yields keys which are strings → TypeError
        with pytest.raises(TypeError):
            prod_signs({"a": 1})
