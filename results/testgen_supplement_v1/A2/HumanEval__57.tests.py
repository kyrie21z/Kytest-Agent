import pytest
from solution import monotonic


# ──────────────────────────────────────────────
# Normal cases – typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with standard, clearly monotonic / non-monotonic lists."""

    def test_increasing_positive(self):
        """[1, 2, 4, 20] is strictly increasing → True"""
        assert monotonic([1, 2, 4, 20]) is True

    def test_decreasing_with_negative(self):
        """[4, 1, 0, -10] is strictly decreasing → True"""
        assert monotonic([4, 1, 0, -10]) is True

    def test_neither_increasing_nor_decreasing(self):
        """[1, 20, 4, 10] goes up then down → False"""
        assert monotonic([1, 20, 4, 10]) is False

    def test_strictly_increasing(self):
        """[1, 3, 5, 7] is strictly increasing → True"""
        assert monotonic([1, 3, 5, 7]) is True

    def test_strictly_decreasing(self):
        """[9, 6, 3, 0] is strictly decreasing → True"""
        assert monotonic([9, 6, 3, 0]) is True

    def test_two_elements_increasing(self):
        """[1, 2] is increasing → True"""
        assert monotonic([1, 2]) is True

    def test_two_elements_decreasing(self):
        """[2, 1] is decreasing → True"""
        assert monotonic([2, 1]) is True

    def test_two_elements_equal(self):
        """[5, 5] is both non-decreasing and non-increasing → True"""
        assert monotonic([5, 5]) is True


# ──────────────────────────────────────────────
# Boundary cases – edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the boundaries of what constitutes monotonicity."""

    def test_all_same_elements(self):
        """[3, 3, 3, 3] is trivially both increasing & decreasing → True"""
        assert monotonic([3, 3, 3, 3]) is True

    def test_increasing_then_flat(self):
        """[1, 2, 2, 3] never decreases → True"""
        assert monotonic([1, 2, 2, 3]) is True

    def test_decreasing_then_flat(self):
        """[5, 4, 4, 2] never increases → True"""
        assert monotonic([5, 4, 4, 2]) is True

    def test_flat_then_increasing(self):
        """[3, 3, 4, 5] never decreases → True"""
        assert monotonic([3, 3, 4, 5]) is True

    def test_flat_then_decreasing(self):
        """[7, 7, 5, 3] never increases → True"""
        assert monotonic([7, 7, 5, 3]) is True

    def test_single_element(self):
        """A single-element list is trivially monotonic → True"""
        assert monotonic([42]) is True

    def test_large_increasing_list(self):
        """A long strictly increasing list → True"""
        assert monotonic(list(range(1000))) is True

    def test_large_decreasing_list(self):
        """A long strictly decreasing list → True"""
        assert monotonic(list(range(1000, 0, -1))) is True


# ──────────────────────────────────────────────
# Empty / zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyInputs:
    """Tests with empty or minimal-length lists."""

    def test_empty_list(self):
        """An empty list has no violating pairs → True"""
        assert monotonic([]) is True


# ──────────────────────────────────────────────
# Invalid inputs – types that would raise errors
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests that pass truly invalid argument types to verify exceptions."""

    @pytest.mark.parametrize("bad_input", [
        None,
        42,
    ])
    def test_raises_on_non_iterable(self, bad_input):
        """Passing a value without len() should raise TypeError."""
        with pytest.raises(TypeError):
            monotonic(bad_input)


# ──────────────────────────────────────────────
# Exception cases – values that trigger edge logic
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests for unusual value combinations."""

    def test_mixed_signs_increasing(self):
        """[-5, -2, 0, 3] crosses zero but is increasing → True"""
        assert monotonic([-5, -2, 0, 3]) is True

    def test_mixed_signs_decreasing(self):
        """[5, 2, -1, -8] crosses zero but is decreasing → True"""
        assert monotonic([5, 2, -1, -8]) is True

    def test_up_down_up(self):
        """[1, 5, 2, 8] oscillates → False"""
        assert monotonic([1, 5, 2, 8]) is False

    def test_down_up_down(self):
        """[10, 3, 7, 1] oscillates → False"""
        assert monotonic([10, 3, 7, 1]) is False

    def test_ascending_descending_boundary(self):
        """[1, 2, 3, 2, 1] goes up then down → False"""
        assert monotonic([1, 2, 3, 2, 1]) is False

    def test_descending_ascending_boundary(self):
        """[5, 4, 3, 4, 5] goes down then up → False"""
        assert monotonic([5, 4, 3, 4, 5]) is False

    def test_three_elements_equal(self):
        """[7, 7, 7] is trivially monotonic → True"""
        assert monotonic([7, 7, 7]) is True

    def test_alternating_small_values(self):
        """[0, 1, 0, 1] alternates → False"""
        assert monotonic([0, 1, 0, 1]) is False
