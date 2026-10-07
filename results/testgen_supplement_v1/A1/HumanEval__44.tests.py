"""Unit tests for change_base() in solution.py."""

import pytest
from solution import change_base


# ---------------------------------------------------------------------------
# 1. Normal cases – including every doctest example
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Typical, well-documented inputs."""

    def test_doctest_8_to_3(self):
        assert change_base(8, 3) == "22"

    def test_doctest_8_to_2(self):
        assert change_base(8, 2) == "1000"

    def test_doctest_7_to_2(self):
        assert change_base(7, 2) == "111"

    def test_10_to_5(self):
        # 10 decimal = 20 in base 5
        assert change_base(10, 5) == "20"

    def test_100_to_2(self):
        # 100 decimal = 1100100 in binary
        assert change_base(100, 2) == "1100100"

    def test_100_to_8(self):
        # 100 decimal = 144 in octal
        assert change_base(100, 8) == "144"

    def test_255_to_2(self):
        # 255 decimal = 11111111 in binary
        assert change_base(255, 2) == "11111111"

    def test_1000_to_5(self):
        # 1000 decimal = 13000 in base 5
        assert change_base(1000, 5) == "13000"

    def test_all_bases_for_number_6(self):
        """Verify conversion of 6 across every valid base (2-9)."""
        assert change_base(6, 2) == "110"   # 6 = 1*4 + 1*2 + 0
        assert change_base(6, 3) == "20"   # 6 = 2*3 + 0
        assert change_base(6, 4) == "12"   # 6 = 1*4 + 2
        assert change_base(6, 5) == "11"   # 6 = 1*5 + 1
        assert change_base(6, 6) == "10"   # 6 = 1*6 + 0
        assert change_base(6, 7) == "6"
        assert change_base(6, 8) == "6"
        assert change_base(6, 9) == "6"


# ---------------------------------------------------------------------------
# 2. Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Edge-of-range inputs."""

    def test_x_equals_zero(self):
        """x=0 is explicitly handled in the source."""
        assert change_base(0, 2) == "0"
        assert change_base(0, 5) == "0"
        assert change_base(0, 9) == "0"

    def test_x_equals_one(self):
        """Smallest positive integer."""
        assert change_base(1, 2) == "1"
        assert change_base(1, 9) == "1"

    def test_min_base(self):
        """base=2 is the smallest valid base per docstring."""
        assert change_base(3, 2) == "11"
        assert change_base(10, 2) == "1010"

    def test_max_base(self):
        """base=9 is the largest valid base (< 10) per docstring."""
        assert change_base(9, 9) == "10"
        assert change_base(80, 9) == "88"  # 80 = 8*9 + 8

    def test_large_number(self):
        """A larger number to ensure multi-digit correctness."""
        assert change_base(1000000, 2) == "11110100001001000000"
        assert change_base(1000000, 8) == "3641100"

    def test_base_greater_than_number(self):
        """When base > x, result is just the single digit."""
        assert change_base(3, 5) == "3"
        assert change_base(1, 9) == "1"


# ---------------------------------------------------------------------------
# 3. Empty / null / zero-size inputs
# ---------------------------------------------------------------------------

class TestZeroAndNullInputs:
    """Special zero-value handling."""

    def test_zero_x_various_bases(self):
        """x=0 should always return '0' regardless of base."""
        for base in range(2, 10):
            assert change_base(0, base) == "0"


# ---------------------------------------------------------------------------
# 4. Invalid inputs – violating documented constraints
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Inputs that violate the docstring's implied constraints."""

    @pytest.mark.parametrize("base", [0])
    def test_base_zero_raises_zero_division_error(self, base):
        """Base=0 causes ZeroDivisionError via x % 0."""
        with pytest.raises(ZeroDivisionError):
            change_base(10, base)

    def test_base_negative_infinite_loop(self):
        """Negative base causes infinite loop; we skip actual execution.

        The docstring states 'base numbers are less than 10', implying
        base >= 1. With base < 0, Python's floor division makes the
        while-loop condition `x != 0` never reach a terminal state for
        many inputs (e.g., base=-1 oscillates). We simply assert that
        negative bases are *not* part of the supported API.
        """
        # Do NOT call change_base with negative base — it hangs.
        # This test documents the expected contract violation.
        pass

    @pytest.mark.parametrize("base", [10, 16, 100])
    def test_base_greater_than_or_equal_to_10(self, base):
        """Docstring says 'base numbers are less than 10'.

        For base=10 the function effectively returns str(x), which is
        outside the intended scope. For base>=10 no exception is raised
        but the output is not a proper base-N representation.
        """
        result = change_base(10, base)
        assert isinstance(result, str)
        # base=10: returns "10" which is just str(10), not a converted form
        if base == 10:
            assert result == "10"

    def test_negative_x(self):
        """Negative x is not documented; test actual behaviour.

        With negative x and positive base, Python's // floors toward -inf.
        The loop eventually reaches 0 after several iterations.
        """
        result = change_base(-8, 2)
        assert isinstance(result, str)
        # The result will be some string; exact value depends on implementation
        # but it should not crash.
        assert len(result) > 0


# ---------------------------------------------------------------------------
# 5. Exception cases
# ---------------------------------------------------------------------------

class TestExceptionCases:
    """Cases where exceptions may be raised."""

    def test_base_zero_raises_zero_division_error(self):
        """x % 0 raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            change_base(10, 0)

    def test_base_one_infinite_loop(self):
        """base=1 causes infinite loop: x % 1 == 0 always, x //= 1 never changes x.

        The docstring implies base >= 2. base=1 is degenerate.
        We skip actual execution to avoid hanging.
        """
        # Do NOT call change_base(10, 1) — it hangs.
        pass
