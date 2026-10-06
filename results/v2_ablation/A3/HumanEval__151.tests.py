import pytest
from solution import double_the_difference


# ──────────────────────────────────────────────
# 1. Normal / typical inputs
# ──────────────────────────────────────────────

class TestNormalCases:
    """Typical inputs matching the docstring examples."""

    def test_docstring_example_1(self):
        # [1, 3, 2, 0] → 1² + 3² + 0 + 0 = 10
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_docstring_example_2(self):
        # [-1, -2, 0] → all ignored → 0
        assert double_the_difference([-1, -2, 0]) == 0

    def test_docstring_example_3(self):
        # [9, -2] → 9² = 81
        assert double_the_difference([9, -2]) == 81

    def test_docstring_example_4(self):
        # [0] → 0
        assert double_the_difference([0]) == 0

    def test_single_odd_positive(self):
        # [1] → 1² = 1
        assert double_the_difference([1]) == 1

    def test_multiple_odds(self):
        # [1, 3, 5] → 1 + 9 + 25 = 35
        assert double_the_difference([1, 3, 5]) == 35

    def test_mixed_even_and_odd(self):
        # [2, 3, 4, 5] → 3² + 5² = 9 + 25 = 34
        assert double_the_difference([2, 3, 4, 5]) == 34

    def test_large_odd_number(self):
        # [999] → 999² = 998001
        assert double_the_difference([999]) == 998001

    def test_all_evens(self):
        # [2, 4, 6, 8] → none are odd → 0
        assert double_the_difference([2, 4, 6, 8]) == 0


# ──────────────────────────────────────────────
# 2. Boundary cases at edges of valid ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Inputs at the boundaries of the valid range."""

    def test_smallest_positive_odd(self):
        # 1 is the smallest positive odd integer
        assert double_the_difference([1]) == 1

    def test_largest_positive_odd(self):
        # A very large odd number
        assert double_the_difference([100001]) == 100001 ** 2  # 10000200001

    def test_negative_one(self):
        # -1 is odd but negative → ignored
        assert double_the_difference([-1]) == 0

    def test_negative_odd_numbers(self):
        # [-3, -5, -7] → all negative → 0
        assert double_the_difference([-3, -5, -7]) == 0

    def test_zero(self):
        # 0 is even → ignored
        assert double_the_difference([0]) == 0

    def test_only_zeros(self):
        # [0, 0, 0] → all zeros → 0
        assert double_the_difference([0, 0, 0]) == 0

    def test_alternating_odd_even(self):
        # [1, 2, 3, 4, 5] → 1² + 3² + 5² = 1 + 9 + 25 = 35
        assert double_the_difference([1, 2, 3, 4, 5]) == 35


# ──────────────────────────────────────────────
# 3. Empty, null, or zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyAndZeroSizeInputs:
    """Edge cases involving empty or zero-size inputs."""

    def test_empty_list(self):
        assert double_the_difference([]) == 0

    def test_single_element_list_with_zero(self):
        assert double_the_difference([0]) == 0


# ──────────────────────────────────────────────
# 4. Invalid / non-integer inputs
# ──────────────────────────────────────────────

class TestNonIntegerInputs:
    """Inputs that are not valid integers (floats, etc.)."""

    def test_float_values(self):
        # [1.5, 3.7] → floats have "." in str() → ignored
        assert double_the_difference([1.5, 3.7]) == 0

    def test_integer_like_float(self):
        # [2.0, 4.0] → ".0" in str → ignored
        assert double_the_difference([2.0, 4.0]) == 0

    def test_mixed_int_and_float(self):
        # [1, 2.5, 3, 4.0] → 1² + 3² = 10
        assert double_the_difference([1, 2.5, 3, 4.0]) == 10

    def test_negative_float(self):
        # [-1.5, -3.7] → floats → ignored
        assert double_the_difference([-1.5, -3.7]) == 0

    def test_string_in_list(self):
        # Strings will cause TypeError when num % 2 is evaluated
        with pytest.raises(TypeError):
            double_the_difference(["1", "3"])

    def test_none_in_list(self):
        # None will cause TypeError when num % 2 is evaluated
        with pytest.raises(TypeError):
            double_the_difference([None])

    def test_boolean_true(self):
        # True % 2 == 1, True > 0, str(True)="True" no "." → counted as 1²
        assert double_the_difference([True]) == 1

    def test_boolean_false(self):
        # False % 2 == 0 → not odd → ignored
        assert double_the_difference([False]) == 0

    def test_mixed_bool_and_int(self):
        # [True, 1, False, 3] → True→1, 1→1, False→ignored, 3→9 = 1+1+9 = 11
        assert double_the_difference([True, 1, False, 3]) == 11


# ──────────────────────────────────────────────
# 5. Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Inputs that trigger exceptions."""

    def test_list_with_strings_raises_typeerror(self):
        with pytest.raises(TypeError):
            double_the_difference(["hello", "world"])

    def test_list_with_none_raises_typeerror(self):
        with pytest.raises(TypeError):
            double_the_difference([1, None, 3])

    def test_list_with_complex_numbers_raises_typeerror(self):
        with pytest.raises(TypeError):
            double_the_difference([1 + 2j])

    def test_list_with_tuples_raises_typeerror(self):
        with pytest.raises(TypeError):
            double_the_difference([(1, 2)])

    def test_non_list_input_raises_typeerror(self):
        # Passing a non-list iterable; tuples work element-wise but
        # passing a string iterates over characters → TypeError
        with pytest.raises(TypeError):
            double_the_difference("123")


# ──────────────────────────────────────────────
# 6. Additional correctness / sanity checks
# ──────────────────────────────────────────────

class TestAdditionalCorrectness:
    """Extra cases to ensure correctness across diverse scenarios."""

    def test_all_same_odd_number(self):
        # [3, 3, 3] → 9 + 9 + 9 = 27
        assert double_the_difference([3, 3, 3]) == 27

    def test_wide_range(self):
        # [-10, -5, -1, 0, 1, 5, 10, 15]
        # positives odds: 1, 5, 15 → 1 + 25 + 225 = 251
        assert double_the_difference([-10, -5, -1, 0, 1, 5, 10, 15]) == 251

    def test_many_elements(self):
        # Sum of squares of all odd numbers from 1 to 99
        lst = list(range(1, 100))
        expected = sum(n ** 2 for n in lst if n % 2 == 1)
        assert double_the_difference(lst) == expected

    def test_negative_then_positive_odds(self):
        # [-3, 1, -5, 3, -7, 5] → 1² + 3² + 5² = 1 + 9 + 25 = 35
        assert double_the_difference([-3, 1, -5, 3, -7, 5]) == 35

    def test_duplicate_odds(self):
        # [1, 1, 1] → 1 + 1 + 1 = 3
        assert double_the_difference([1, 1, 1]) == 3
