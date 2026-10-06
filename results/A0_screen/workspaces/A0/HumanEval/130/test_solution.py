"""Unit tests for solution.tri() — Tribonacci sequence generator."""

from solution import tri


# ---------------------------------------------------------------------------
# Basic correctness tests – known outputs
# ---------------------------------------------------------------------------

class TestBasicOutputs:
    """Verify exact output for small inputs."""

    def test_tri_0(self):
        assert tri(0) == [1]

    def test_tri_1(self):
        assert tri(1) == [1, 3]

    def test_tri_2(self):
        # i=2 (even): 1 + 2/2 = 2.0
        assert tri(2) == [1, 3, 2.0]

    def test_tri_3(self):
        # i=3 (odd): ans[-1]+ans[-2]+1+(3+1)/2 = 2.0+3+1+2.0 = 8.0
        assert tri(3) == [1, 3, 2.0, 8.0]

    def test_tri_4(self):
        # i=4 (even): 1 + 4/2 = 3.0
        assert tri(4) == [1, 3, 2.0, 8.0, 3.0]

    def test_tri_5(self):
        # i=5 (odd): 3.0 + 8.0 + 1 + (5+1)/2 = 15.0
        assert tri(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]

    def test_tri_6(self):
        # i=6 (even): 1 + 6/2 = 4.0
        assert tri(6) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0]

    def test_tri_7(self):
        # i=7 (odd): 4.0 + 15.0 + 1 + (7+1)/2 = 24.0
        assert tri(7) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0]

    def test_tri_8(self):
        # i=8 (even): 1 + 8/2 = 5.0
        assert tri(8) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0]

    def test_tri_9(self):
        # i=9 (odd): 5.0 + 24.0 + 1 + (9+1)/2 = 35.0
        assert tri(9) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0, 35.0]


# ---------------------------------------------------------------------------
# Return type & structure tests
# ---------------------------------------------------------------------------

class TestReturnType:
    """Check that the function always returns a list."""

    def test_returns_list(self):
        assert isinstance(tri(0), list)
        assert isinstance(tri(1), list)
        assert isinstance(tri(10), list)

    def test_length_is_n_plus_1(self):
        for n in range(0, 20):
            result = tri(n)
            assert len(result) == n + 1, f"Expected length {n+1} for n={n}, got {len(result)}"

    def test_first_element_always_one(self):
        for n in range(0, 20):
            assert tri(n)[0] == 1

    def test_second_element_always_three(self):
        for n in range(1, 20):
            assert tri(n)[1] == 3


# ---------------------------------------------------------------------------
# Recurrence relation tests
# ---------------------------------------------------------------------------

class TestRecurrenceRelation:
    """Verify the recurrence rules are followed correctly."""

    def test_even_index_rule(self):
        """For even i >= 2: value should be 1 + i/2."""
        for n in range(2, 20, 2):
            result = tri(n)
            expected = 1 + n / 2
            assert result[n] == expected, f"Even index {n}: expected {expected}, got {result[n]}"

    def test_odd_index_rule(self):
        """For odd i >= 3: value should be sum of previous two + 1 + (i+1)/2."""
        for n in range(3, 20, 2):
            result = tri(n)
            expected = result[n - 1] + result[n - 2] + 1 + (n + 1) / 2
            assert result[n] == expected, f"Odd index {n}: expected {expected}, got {result[n]}"

    def test_all_even_positions(self):
        """Every element at an even index follows the even rule."""
        result = tri(10)
        for i in range(2, 11, 2):
            assert result[i] == 1 + i / 2

    def test_all_odd_positions(self):
        """Every element at an odd index follows the odd rule."""
        result = tri(11)
        for i in range(3, 12, 2):
            expected = result[i - 1] + result[i - 2] + 1 + (i + 1) / 2
            assert result[i] == expected


# ---------------------------------------------------------------------------
# Element type tests
# ---------------------------------------------------------------------------

class TestElementTypes:
    """Check types of returned elements."""

    def test_first_two_elements_are_integers(self):
        """First two elements are hardcoded as ints."""
        for n in range(2, 20):
            result = tri(n)
            assert isinstance(result[0], int), f"result[0] should be int, got {type(result[0])}"
            assert isinstance(result[1], int), f"result[1] should be int, got {type(result[1])}"

    def test_remaining_elements_are_floats(self):
        """Elements from index 2 onward use float division."""
        for n in range(2, 20):
            result = tri(n)
            for i in range(2, len(result)):
                assert isinstance(result[i], float), \
                    f"result[{i}] should be float, got {type(result[i])}"


# ---------------------------------------------------------------------------
# Monotonicity / growth tests
# ---------------------------------------------------------------------------

class TestGrowthProperties:
    """Check general properties of the sequence growth."""

    def test_sequence_is_non_decreasing_from_index_2(self):
        """After index 2, values generally grow (not strictly monotone due to even rule dips)."""
        result = tri(15)
        # Even-indexed values follow 1+i/2 which grows linearly
        # Odd-indexed values accumulate sums, growing faster
        for i in range(2, len(result) - 1):
            if i % 2 == 0:
                # Even: next value could be smaller (e.g., tri(4)=3 < tri(3)=8)
                pass
            else:
                # Odd: accumulated sum, should be larger than last
                assert result[i] > result[i - 1], \
                    f"Odd index {i}: expected {result[i]} > {result[i-1]}"

    def test_values_are_positive(self):
        """All values in the sequence should be positive."""
        for n in range(0, 30):
            result = tri(n)
            for val in result:
                assert val > 0, f"Found non-positive value {val} in tri({n})"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Test edge and boundary conditions."""

    def test_zero_input(self):
        assert tri(0) == [1]

    def test_single_element_return_for_n_0(self):
        assert len(tri(0)) == 1

    def test_large_input(self):
        """Test with a moderately large input to ensure no overflow/recursion issues."""
        result = tri(50)
        assert len(result) == 51
        assert result[0] == 1
        assert result[1] == 3
        # Verify last few elements exist and are positive
        assert all(v > 0 for v in result)

    def test_consistency_across_calls(self):
        """Calling tri(n) multiple times should yield identical results."""
        for n in [0, 1, 5, 10, 20]:
            assert tri(n) == tri(n)


# ---------------------------------------------------------------------------
# Parametrized tests
# ---------------------------------------------------------------------------

import pytest


@pytest.mark.parametrize("n,expected", [
    (0, [1]),
    (1, [1, 3]),
    (2, [1, 3, 2.0]),
    (3, [1, 3, 2.0, 8.0]),
    (4, [1, 3, 2.0, 8.0, 3.0]),
    (5, [1, 3, 2.0, 8.0, 3.0, 15.0]),
    (10, [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0, 35.0, 6.0]),
])
def test_parametrized(n, expected):
    assert tri(n) == expected
