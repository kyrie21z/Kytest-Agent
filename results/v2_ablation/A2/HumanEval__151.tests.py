"""Unit tests for solution.double_the_difference."""

import pytest
from solution import double_the_difference


class TestNormalCases:
    """Tests with typical valid inputs."""

    def test_simple_odd_numbers(self):
        """Sum of squares of positive odd integers."""
        assert double_the_difference([1, 3, 2, 0]) == 10  # 1^2 + 3^2 = 10

    def test_single_odd_number(self):
        """Single positive odd number."""
        assert double_the_difference([5]) == 25  # 5^2 = 25

    def test_multiple_odd_numbers(self):
        """Multiple positive odd numbers mixed with evens."""
        assert double_the_difference([1, 3, 5, 7]) == 84  # 1+9+25+49 = 84

    def test_even_numbers_only(self):
        """Only even numbers — should return 0."""
        assert double_the_difference([2, 4, 6, 8]) == 0

    def test_mixed_positive_and_negative_odds(self):
        """Positive odds included, negative odds excluded."""
        assert double_the_difference([9, -2]) == 81  # only 9^2 = 81

    def test_negative_odds_excluded(self):
        """Negative odd numbers are ignored."""
        assert double_the_difference([-1, -3, -7]) == 0

    def test_all_zeros(self):
        """All zeros — even, so excluded."""
        assert double_the_difference([0, 0, 0]) == 0

    def test_large_odd_number(self):
        """A larger odd number squared."""
        assert double_the_difference([11]) == 121  # 11^2 = 121

    def test_mixed_with_evens_and_odds(self):
        """Mix of positive odds and evens."""
        assert double_the_difference([1, 2, 3, 4, 5]) == 35  # 1+9+25 = 35


class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_smallest_positive_odd(self):
        """Smallest positive odd number: 1."""
        assert double_the_difference([1]) == 1  # 1^2 = 1

    def test_largest_common_odd(self):
        """Larger odd number near common range limits."""
        assert double_the_difference([99]) == 9801  # 99^2 = 9801

    def test_boundary_between_even_and_odd(self):
        """Numbers around the even/odd boundary."""
        assert double_the_difference([3, 4, 5]) == 34  # 9 + 25 = 34

    def test_zero_is_not_included(self):
        """Zero is even, not odd, so excluded."""
        assert double_the_difference([0]) == 0

    def test_one_is_included(self):
        """One is the smallest positive odd."""
        assert double_the_difference([1, 2]) == 1  # only 1^2 = 1


class TestEmptyAndNullInputs:
    """Tests for empty, null, or zero-size inputs."""

    def test_empty_list(self):
        """Empty list returns 0."""
        assert double_the_difference([]) == 0

    def test_none_input_raises(self):
        """Passing None should raise TypeError."""
        with pytest.raises(TypeError):
            double_the_difference(None)


class TestInvalidInputs:
    """Tests for invalid or edge-case inputs that the function may encounter."""

    def test_float_values_excluded(self):
        """Float values like 1.5 are excluded because '.' in str()."""
        assert double_the_difference([1.5, 3.7]) == 0

    def test_integer_floats_excluded(self):
        """Floats representing whole numbers (e.g., 2.0) are excluded."""
        assert double_the_difference([2.0, 4.0]) == 0

    def test_string_values_excluded(self):
        """String representations of numbers are not processed as integers."""
        # str("3") contains no '.', "3" % 2 raises TypeError in Python 3
        # But actually, "3" % 2 would raise TypeError, so we expect it to fail
        with pytest.raises(TypeError):
            double_the_difference(["3", "5"])

    def test_boolean_values(self):
        """Booleans: True == 1, False == 0. In Python, bool is subclass of int."""
        # True % 2 == 1, True > 0, "." not in str(True) -> "True" has no dot
        # So True is treated as 1 and included.
        assert double_the_difference([True]) == 1  # True acts as 1, 1^2 = 1

    def test_false_value(self):
        """False == 0, which is even, so excluded."""
        assert double_the_difference([False]) == 0

    def test_negative_float(self):
        """Negative floats are excluded."""
        assert double_the_difference([-1.5, -3.7]) == 0

    def test_very_large_list(self):
        """Large list with many elements."""
        lst = list(range(1, 101))  # 1 to 100
        # Sum of squares of all odd numbers from 1 to 99
        expected = sum(i ** 2 for i in range(1, 100, 2))
        assert double_the_difference(lst) == expected

    def test_duplicate_odd_numbers(self):
        """Duplicate odd numbers each contribute their square."""
        assert double_the_difference([3, 3, 3]) == 27  # 9 + 9 + 9 = 27


class TestExceptionCases:
    """Tests where the function can raise exceptions."""

    def test_non_iterable_raises(self):
        """Passing a non-iterable should raise TypeError."""
        with pytest.raises(TypeError):
            double_the_difference(42)

    def test_dict_raises(self):
        """Passing a dict iterates over keys, which may cause issues."""
        # dict keys are iterated; if they're strings, str(key) % 2 raises TypeError
        with pytest.raises(TypeError):
            double_the_difference({"a": 1})

    def test_tuple_works(self):
        """Tuples are iterable and should work fine."""
        assert double_the_difference((1, 3, 5)) == 35  # 1+9+25 = 35

    def test_generator_works(self):
        """Generators are iterable and should work."""
        gen = (x for x in [1, 3, 5])
        assert double_the_difference(gen) == 35  # 1+9+25 = 35
