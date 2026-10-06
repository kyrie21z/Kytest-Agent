"""Unit tests for count_up_to in solution.py."""

import pytest
from solution import count_up_to


# ---------------------------------------------------------------------------
# Documented example cases from the docstring
# ---------------------------------------------------------------------------

class TestDocumentedExamples:
    """Tests taken directly from the function's docstring."""

    def test_count_up_to_5(self):
        assert count_up_to(5) == [2, 3]

    def test_count_up_to_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_count_up_to_0(self):
        assert count_up_to(0) == []

    def test_count_up_to_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_count_up_to_1(self):
        assert count_up_to(1) == []

    def test_count_up_to_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]


# ---------------------------------------------------------------------------
# Boundary cases at the edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of the valid input domain."""

    def test_n_is_two(self):
        """Smallest n where there is exactly one prime (< 2)."""
        assert count_up_to(2) == []

    def test_n_is_three(self):
        """Only prime strictly less than 3 is 2."""
        assert count_up_to(3) == [2]

    def test_n_is_four(self):
        assert count_up_to(4) == [2, 3]

    def test_n_is_six(self):
        assert count_up_to(6) == [2, 3, 5]

    def test_n_is_ten(self):
        assert count_up_to(10) == [2, 3, 5, 7]

    def test_n_is_seventy(self):
        primes_below_70 = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67,
        ]
        assert count_up_to(70) == primes_below_70

    def test_n_is_one_hundred(self):
        primes_below_100 = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]
        assert count_up_to(100) == primes_below_100


# ---------------------------------------------------------------------------
# Empty / zero-size inputs
# ---------------------------------------------------------------------------

class TestZeroAndEmptyInputs:
    """Tests for inputs that produce empty results."""

    def test_zero_returns_empty_list(self):
        assert count_up_to(0) == []
        assert isinstance(count_up_to(0), list)

    def test_one_returns_empty_list(self):
        assert count_up_to(1) == []

    def test_two_returns_empty_list(self):
        assert count_up_to(2) == []


# ---------------------------------------------------------------------------
# Invalid inputs – the docstring specifies a non-negative integer
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests for inputs outside the documented contract."""

    @pytest.mark.parametrize("value", [-1, -5, -100])
    def test_negative_integer_returns_empty_list(self, value):
        """Negative integers result in an empty list (the range is empty)."""
        assert count_up_to(value) == []

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            count_up_to(None)

    @pytest.mark.parametrize("value", ["five", "", "abc"])
    def test_string_raises_type_error(self, value):
        with pytest.raises(TypeError):
            count_up_to(value)

    @pytest.mark.parametrize("value", [3.14, 0.0, 1.5])
    def test_float_raises_type_error(self, value):
        """Floats cannot be used as list size; expect TypeError."""
        with pytest.raises(TypeError):
            count_up_to(value)


# ---------------------------------------------------------------------------
# Additional correctness checks
# ---------------------------------------------------------------------------

class TestCorrectnessProperties:
    """Property-based sanity checks on the output."""

    def test_all_results_are_less_than_n(self):
        """Every returned prime must be strictly less than n."""
        for n in range(2, 50):
            result = count_up_to(n)
            assert all(p < n for p in result), f"Failed for n={n}"

    def test_no_composites_in_result(self):
        """No composite number should appear in the result."""
        for n in range(2, 100):
            result = count_up_to(n)
            for p in result:
                for d in range(2, int(p**0.5) + 1):
                    assert p % d != 0, f"{p} is composite but appeared for n={n}"

    def test_result_is_sorted(self):
        """The list of primes should be in ascending order."""
        for n in [5, 10, 20, 50, 100]:
            result = count_up_to(n)
            assert result == sorted(result)

    def test_consistency_across_n_values(self):
        """count_up_to(n) should always be a prefix of count_up_to(m) for m > n."""
        for n in range(2, 30):
            for m in range(n + 1, 30):
                result_n = count_up_to(n)
                result_m = count_up_to(m)
                assert result_n == result_m[:len(result_n)], \
                    f"Prefix mismatch: n={n}, m={m}"
