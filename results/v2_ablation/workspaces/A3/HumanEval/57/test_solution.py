"""Unit tests for the monotonic() function in solution.py."""

import pytest
from solution import monotonic


# ──────────────────────────────────────────────
# Normal / typical inputs
# ──────────────────────────────────────────────

class TestMonotonicIncreasing:
    """Tests for strictly and non-strictly increasing lists."""

    def test_strictly_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_non_decreasing_with_duplicates(self):
        assert monotonic([1, 2, 2, 3]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_all_equal(self):
        assert monotonic([7, 7, 7, 7]) is True

    def test_single_element(self):
        assert monotonic([5]) is True

    def test_empty_list(self):
        assert monotonic([]) is True

    def test_negative_numbers_increasing(self):
        assert monotonic([-5, -3, -1]) is True

    def test_mixed_sign_increasing(self):
        assert monotonic([-1, 0, 1, 2]) is True

    def test_floats_increasing(self):
        assert monotonic([1.5, 2.5, 3.5]) is True

    def test_large_increasing_range(self):
        assert monotonic(list(range(1000))) is True


class TestMonotonicDecreasing:
    """Tests for strictly and non-strictly decreasing lists."""

    def test_strictly_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_non_increasing_with_duplicates(self):
        assert monotonic([5, 4, 4, 2]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([2, 1]) is True

    def test_negative_numbers_decreasing(self):
        assert monotonic([-1, -3, -5]) is True

    def test_mixed_sign_decreasing(self):
        assert monotonic([5, 0, -3, -10]) is True

    def test_floats_decreasing(self):
        assert monotonic([5.5, 3.3, 1.1]) is True

    def test_large_decreasing_range(self):
        assert monotonic(list(range(1000, 0, -1))) is True


# ──────────────────────────────────────────────
# Boundary cases at edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at boundaries of valid input ranges."""

    def test_two_equal_elements(self):
        assert monotonic([3, 3]) is True

    def test_three_elements_first_equals_last(self):
        # [1, 5, 1] — goes up then down → not monotonic
        assert monotonic([1, 5, 1]) is False

    def test_three_elements_middle_equals_edge(self):
        # [1, 1, 5] — flat then up → non-decreasing → True
        assert monotonic([1, 1, 5]) is True

    def test_four_elements_plateau_then_drop(self):
        # [3, 3, 3, 1] — non-increasing → True
        assert monotonic([3, 3, 3, 1]) is True

    def test_alternating_up_down_early(self):
        # [1, 3, 2, 4] — not monotonic
        assert monotonic([1, 3, 2, 4]) is False

    def test_alternating_up_down_late(self):
        # [1, 2, 3, 1] — not monotonic
        assert monotonic([1, 2, 3, 1]) is False


# ──────────────────────────────────────────────
# Invalid / edge-case inputs
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests for inputs that should raise errors or behave gracefully."""

    def test_none_input_raises_type_error(self):
        with pytest.raises(TypeError):
            monotonic(None)

    def test_string_input_works(self):
        """Strings are iterable and character comparison works in Python.
           'a' < 'b' < 'c', so 'abc' is monotonically increasing."""
        assert monotonic("abc") is True

    def test_tuple_input(self):
        """Tuples support comparison; this should work like a list."""
        assert monotonic((1, 2, 3)) is True

    def test_generator_input_raises_type_error(self):
        """Generators do not support len(), so the function raises TypeError."""
        gen = (x for x in [1, 2, 3])
        with pytest.raises(TypeError):
            monotonic(gen)


# ──────────────────────────────────────────────
# Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_unordered_elements_raise_type_error(self):
        """Mixing incomparable types raises TypeError."""
        with pytest.raises(TypeError):
            monotonic([1, "a", 3])

    def test_dict_values_unordered(self):
        d = {3: 'c', 1: 'a', 2: 'b'}
        # dict keys are ordered in Python 3.7+, giving [3, 1, 2] which is not monotonic
        assert monotonic(list(d.keys())) is False

    def test_set_input_raises_type_error(self):
        """Sets are unordered and don't support indexing via len/range pattern."""
        with pytest.raises(TypeError):
            monotonic({3, 1, 2})


# ──────────────────────────────────────────────
# Doctest examples from the docstring
# ──────────────────────────────────────────────

class TestDocstringExamples:
    """Verify the exact examples from the function's docstring."""

    def test_docstring_example_1(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_docstring_example_2(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_docstring_example_3(self):
        assert monotonic([4, 1, 0, -10]) is True
