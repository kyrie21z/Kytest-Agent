"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


class TestNormalCases:
    """Tests with typical valid inputs."""

    def test_simple_odds(self):
        """Sum of squares of positive odd integers."""
        assert double_the_difference([1, 3, 2, 0]) == 10  # 1² + 3² = 10

    def test_single_odd(self):
        """Single positive odd number."""
        assert double_the_difference([5]) == 25  # 5² = 25

    def test_multiple_odds(self):
        """Multiple positive odd numbers."""
        assert double_the_difference([1, 3, 5]) == 35  # 1² + 3² + 5² = 1+9+25=35

    def test_odds_with_evens_and_zeros(self):
        """Odds mixed with evens and zeros; only odds counted."""
        assert double_the_difference([1, 2, 4, 6, 7]) == 50  # 1² + 7² = 1+49=50

    def test_negative_and_positive_mix(self):
        """Negative numbers are ignored; only positive odds count."""
        assert double_the_difference([9, -2]) == 81  # 9² = 81

    def test_all_negatives(self):
        """All negatives — nothing qualifies."""
        assert double_the_difference([-1, -3, -5]) == 0

    def test_all_evens(self):
        """All even numbers — nothing qualifies."""
        assert double_the_difference([2, 4, 6, 8]) == 0

    def test_mixed_large_values(self):
        """Larger positive odd numbers."""
        assert double_the_difference([3, 7, 11]) == 179  # 9 + 49 + 121 = 179

    def test_docstring_example_1(self):
        """Verify docstring example: [1, 3, 2, 0] == 10."""
        assert double_the_difference([1, 3, 2, 0]) == 10

    def test_docstring_example_2(self):
        """Verify docstring example: [-1, -2, 0] == 0."""
        assert double_the_difference([-1, -2, 0]) == 0

    def test_docstring_example_3(self):
        """Verify docstring example: [9, -2] == 81."""
        assert double_the_difference([9, -2]) == 81

    def test_docstring_example_4(self):
        """Verify docstring example: [0] == 0."""
        assert double_the_difference([0]) == 0

    def test_mixed_list(self):
        """Mixed list: positive odds 1, 3, 5, 7 contribute."""
        assert double_the_difference([1, 2, 3, 4, 5, 6, 7]) == 84  # 1² + 3² + 5² + 7² = 1+9+25+49=84


class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_odd(self):
        """Smallest positive odd integer: 1."""
        assert double_the_difference([1]) == 1  # 1² = 1

    def test_largest_common_odd(self):
        """A large positive odd number."""
        assert double_the_difference([999]) == 998001  # 999² = 998001

    def test_two_element_list_one_odd(self):
        """Two elements, only one is a qualifying odd."""
        assert double_the_difference([3, 4]) == 9  # 3² = 9

    def test_two_element_list_both_odd(self):
        """Two elements, both are qualifying odds."""
        assert double_the_difference([1, 3]) == 10  # 1² + 3² = 10

    def test_zero_is_not_counted(self):
        """Zero is neither odd nor positive; should be ignored."""
        assert double_the_difference([0, 0, 0]) == 0

    def test_negative_odd_is_not_counted(self):
        """Negative odd numbers are ignored (num > 0 check)."""
        assert double_the_difference([-1, -3, -5]) == 0

    def test_even_positive_not_counted(self):
        """Positive even numbers are ignored (num % 2 == 1 check)."""
        assert double_the_difference([2, 4, 6]) == 0


class TestEmptyAndNullInputs:
    """Tests for empty, null, or zero-size inputs."""

    def test_empty_list(self):
        """Empty list returns 0."""
        assert double_the_difference([]) == 0

    def test_none_input(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            double_the_difference(None)


class TestInvalidInputs:
    """Tests for invalid / unexpected input types."""

    def test_float_values(self):
        """Float values are ignored because '.' in str(num) catches them."""
        assert double_the_difference([1.5, 3.7]) == 0

    def test_float_that_looks_like_odd(self):
        """Even if float value is numerically odd-like, it's ignored."""
        assert double_the_difference([3.0]) == 0

    def test_string_in_list(self):
        """Strings in the list will cause an error when % operator is applied."""
        with pytest.raises(TypeError):
            double_the_difference(["1", "3"])

    def test_mixed_types_with_strings(self):
        """Mix of ints and strings."""
        with pytest.raises(TypeError):
            double_the_difference([1, "hello", 3])

    def test_boolean_values(self):
        """Booleans: True is 1 (odd, positive), False is 0 (not odd)."""
        # In Python, bool is a subclass of int: True == 1, False == 0
        # True % 2 == 1 and True > 0, so True counts as 1
        # False % 2 == 0, so False is ignored
        assert double_the_difference([True, False]) == 1  # True² = 1

    def test_tuple_instead_of_list(self):
        """Tuples are iterable like lists; should work similarly."""
        assert double_the_difference((1, 3, 2)) == 10

    def test_generator_input(self):
        """Generator expressions can be iterated over."""
        result = double_the_difference(x for x in [1, 3, 5])
        assert result == 35  # 1² + 3² + 5² = 35


class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_non_iterable_input(self):
        """Passing a non-iterable should raise TypeError."""
        with pytest.raises(TypeError):
            double_the_difference(42)

    def test_dict_input(self):
        """Dicts iterate over keys; if they're ints, they'll be processed."""
        result = double_the_difference({1: "a", 3: "b"})
        assert result == 10  # 1² + 3² = 10

    def test_nested_list(self):
        """Nested lists will fail when trying % on a list."""
        with pytest.raises(TypeError):
            double_the_difference([[1, 3], [5]])

    def test_complex_numbers(self):
        """Complex numbers don't support % in the same way."""
        with pytest.raises(TypeError):
            double_the_difference([1+2j])

    def test_nan_value(self):
        """NaN % 2 returns nan, which != 1, so NaN is silently ignored."""
        assert double_the_difference([float('nan')]) == 0

    def test_inf_value(self):
        """Inf % 2 returns nan, which != 1, so inf is silently ignored."""
        assert double_the_difference([float('inf')]) == 0
