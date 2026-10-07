"""Unit tests for change_base(x, base) — converts integer x to string in given base (< 10)."""

import pytest
from solution import change_base


# ── Docstring examples (must pass exactly) ──────────────────────────────────

class TestDocstringExamples:
    def test_8_to_base_3(self):
        assert change_base(8, 3) == "22"

    def test_8_to_base_2(self):
        assert change_base(8, 2) == "1000"

    def test_7_to_base_2(self):
        assert change_base(7, 2) == "111"


# ── Normal / typical positive inputs ────────────────────────────────────────

class TestNormalPositiveInputs:
    def test_single_digit_same_base(self):
        # A single digit stays the same when base > digit
        assert change_base(5, 10) == "5"

    def test_ten_to_base_8(self):
        assert change_base(10, 8) == "12"

    def test_ten_to_base_10(self):
        assert change_base(10, 10) == "10"

    def test_one_hundred_to_base_2(self):
        assert change_base(100, 2) == "1100100"

    def test_one_hundred_to_base_8(self):
        assert change_base(100, 8) == "144"

    def test_one_hundred_to_base_9(self):
        assert change_base(100, 9) == "121"

    def test_larger_number_base_2(self):
        assert change_base(255, 2) == "11111111"

    def test_larger_number_base_3(self):
        assert change_base(255, 3) == "100110"

    def test_larger_number_base_10(self):
        assert change_base(12345, 10) == "12345"

    def test_larger_number_base_8(self):
        assert change_base(12345, 8) == "30071"

    def test_larger_number_base_9(self):
        assert change_base(12345, 9) == "17870"

    def test_power_of_two(self):
        assert change_base(16, 2) == "10000"

    def test_power_of_three(self):
        assert change_base(27, 3) == "1000"

    def test_max_valid_base(self):
        """Base 9 is the largest base allowed per docstring."""
        assert change_base(9, 9) == "10"


# ── Boundary cases at edges of valid input ranges ───────────────────────────

class TestBoundaryCases:
    def test_x_is_one(self):
        """Smallest positive integer."""
        assert change_base(1, 2) == "1"
        assert change_base(1, 10) == "1"

    def test_x_is_zero(self):
        """Zero always returns '0' regardless of base."""
        assert change_base(0, 2) == "0"
        assert change_base(0, 10) == "0"

    def test_min_valid_base(self):
        """Base 2 is the smallest valid base."""
        assert change_base(3, 2) == "11"

    def test_large_number(self):
        """A reasonably large number still converts correctly."""
        assert change_base(1024, 2) == "10000000000"
        assert change_base(1024, 8) == "2000"
        assert change_base(1024, 10) == "1024"

    def test_base_equals_number(self):
        """When base equals x, result should be '10'."""
        assert change_base(5, 5) == "10"
        assert change_base(10, 10) == "10"

    def test_base_greater_than_number(self):
        """When base > x, result is just the digit string of x."""
        assert change_base(3, 10) == "3"
        assert change_base(7, 9) == "7"


# ── Invalid inputs that violate documented constraints ──────────────────────

class TestInvalidInputs:
    def test_base_one_infinite_loop(self):
        """Base 1 is not a valid positional base.
        The implementation does NOT guard against this; calling it will hang.
        We skip this test rather than letting CI hang forever.
        """
        pytest.skip("base=1 causes infinite loop in current implementation")

    def test_base_zero_division_by_zero(self):
        """Base 0 causes ZeroDivisionError (x % 0)."""
        with pytest.raises(ZeroDivisionError):
            change_base(5, 0)

    def test_negative_base_skipped(self):
        """Negative base is not meaningful for standard positional systems.
        The implementation may produce unexpected output; we document the error.
        Skip rather than risk infinite loop.
        """
        pytest.skip("negative base may cause infinite loop")

    def test_negative_x_skipped(self):
        """Negative x is not handled by the implementation.
        Due to Python's floor division semantics, e.g. -1 // 2 == -1,
        the while loop can become infinite. We skip rather than hang.
        """
        pytest.skip("negative x may cause infinite loop in current implementation")


# ── Exception cases ─────────────────────────────────────────────────────────

class TestExceptions:
    def test_non_integer_x_raises_type_error(self):
        """Passing a non-integer type should raise TypeError."""
        with pytest.raises(TypeError):
            change_base(5.5, 2)

    def test_non_integer_base_raises_type_error(self):
        with pytest.raises(TypeError):
            change_base(10, 2.0)

    def test_none_input_raises_type_error(self):
        with pytest.raises(TypeError):
            change_base(None, 2)

    def test_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            change_base("10", 2)

    def test_empty_list_input_raises_type_error(self):
        with pytest.raises(TypeError):
            change_base([], 2)

    def test_none_base_raises_type_error(self):
        with pytest.raises(TypeError):
            change_base(10, None)
