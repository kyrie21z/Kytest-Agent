"""Unit tests for prod_signs in solution.py."""

import pytest
from solution import prod_signs


class TestEmptyAndNullInputs:
    """Test edge cases with empty or zero-size inputs."""

    def test_empty_list(self):
        """Empty list should return None per docstring."""
        assert prod_signs([]) is None

    def test_single_zero(self):
        """Single zero element: sign product is 0, so result is 0."""
        assert prod_signs([0]) == 0

    def test_multiple_zeros(self):
        """Multiple zeros: still returns 0."""
        assert prod_signs([0, 0, 0]) == 0


class TestZeroPresence:
    """If any element is 0, the sign product is 0, so result is 0."""

    def test_zero_with_positive_numbers(self):
        assert prod_signs([0, 1]) == 0

    def test_zero_with_negative_numbers(self):
        assert prod_signs([0, -5]) == 0

    def test_zero_in_middle(self):
        assert prod_signs([3, 0, 7]) == 0

    def test_zero_at_end(self):
        assert prod_signs([2, 3, 0]) == 0

    def test_all_zeros(self):
        assert prod_signs([0, 0, 0, 0]) == 0


class TestPositiveOnly:
    """All positive numbers: sign product is +1, result = sum of elements."""

    def test_single_positive(self):
        assert prod_signs([5]) == 5

    def test_multiple_positives(self):
        # [1, 2, 2] -> sum=5, sign_product=+1 -> 5
        assert prod_signs([1, 2, 2]) == 5

    def test_larger_positives(self):
        # [1, 2, 3, 4] -> sum=10, sign_product=+1 -> 10
        assert prod_signs([1, 2, 3, 4]) == 10

    def test_all_ones(self):
        # [1, 1, 1, 1, 1] -> sum=5, sign_product=+1 -> 5
        assert prod_signs([1, 1, 1, 1, 1]) == 5

    def test_single_element_one(self):
        assert prod_signs([1]) == 1


class TestNegativeOnly:
    """All negative numbers: sign product depends on count parity."""

    def test_single_negative(self):
        # [-3] -> sum=3, sign_product=-1 -> -3
        assert prod_signs([-3]) == -3

    def test_two_negatives(self):
        # [-1, -2] -> sum=3, sign_product=(-1)*(-1)=+1 -> 3
        assert prod_signs([-1, -2]) == 3

    def test_three_negatives(self):
        # [-1, -2, -3] -> sum=6, sign_product=(-1)^3=-1 -> -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_four_negatives(self):
        # [-1, -2, -3, -4] -> sum=10, sign_product=(-1)^4=+1 -> 10
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_five_negatives(self):
        # [-1]*5 -> sum=5, sign_product=(-1)^5=-1 -> -5
        assert prod_signs([-1, -1, -1, -1, -1]) == -5

    def test_even_count_large_negatives(self):
        # [-5, -10] -> sum=15, sign_product=+1 -> 15
        assert prod_signs([-5, -10]) == 15

    def test_odd_count_large_negatives(self):
        # [-5, -10, -15] -> sum=30, sign_product=-1 -> -30
        assert prod_signs([-5, -10, -15]) == -30


class TestMixedSigns:
    """Mix of positive and negative numbers."""

    def test_example_from_docstring_one(self):
        # [1, 2, 2, -4] -> sum=9, signs=(+1)(+1)(+1)(-1)=-1 -> -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_example_from_docstring_two(self):
        # [0, 1] -> contains 0 -> 0
        assert prod_signs([0, 1]) == 0

    def test_example_from_docstring_three(self):
        # [] -> None
        assert prod_signs([]) is None

    def test_one_positive_one_negative(self):
        # [3, -2] -> sum=5, sign_product=-1 -> -5
        assert prod_signs([3, -2]) == -5

    def test_two_positives_one_negative(self):
        # [1, 2, -3] -> sum=6, sign_product=-1 -> -6
        assert prod_signs([1, 2, -3]) == -6

    def test_one_positive_two_negatives(self):
        # [1, -2, -3] -> sum=6, sign_product=+1 -> 6
        assert prod_signs([1, -2, -3]) == 6

    def test_mixed_with_larger_values(self):
        # [10, -20, 30] -> sum=60, sign_product=-1 -> -60
        assert prod_signs([10, -20, 30]) == -60

    def test_alternating_signs(self):
        # [1, -1, 1, -1] -> sum=4, sign_product=+1 -> 4
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_many_elements_mixed(self):
        # [1, -2, 3, -4, 5] -> sum=15, sign_product=(-1)^2=+1 -> 15
        assert prod_signs([1, -2, 3, -4, 5]) == 15

    def test_many_elements_mixed_odd_negatives(self):
        # [1, -2, 3, -4, 5, -6] -> sum=21, sign_product=(-1)^3=-1 -> -21
        assert prod_signs([1, -2, 3, -4, 5, -6]) == -21


class TestBoundaryCases:
    """Edge cases at boundaries of valid input ranges."""

    def test_single_element(self):
        assert prod_signs([42]) == 42

    def test_single_negative_element(self):
        assert prod_signs([-42]) == -42

    def test_two_elements_both_positive(self):
        assert prod_signs([1, 1]) == 2

    def test_two_elements_both_negative(self):
        assert prod_signs([-1, -1]) == 2

    def test_two_elements_mixed(self):
        assert prod_signs([1, -1]) == -2

    def test_large_positive_value(self):
        # [1000000] -> sum=1000000, sign_product=+1 -> 1000000
        assert prod_signs([1000000]) == 1000000

    def test_large_negative_value(self):
        # [-1000000] -> sum=1000000, sign_product=-1 -> -1000000
        assert prod_signs([-1000000]) == -1000000

    def test_large_array_all_ones(self):
        arr = [1] * 100
        assert prod_signs(arr) == 100

    def test_large_array_all_negative_ones(self):
        arr = [-1] * 100
        # sum=100, sign_product=(-1)^100=+1 -> 100
        assert prod_signs(arr) == 100

    def test_large_array_odd_negative_ones(self):
        arr = [-1] * 99
        # sum=99, sign_product=(-1)^99=-1 -> -99
        assert prod_signs(arr) == -99


class TestReturnTypes:
    """Verify correct return types."""

    def test_nonempty_returns_int(self):
        assert isinstance(prod_signs([1, 2]), int)

    def test_empty_returns_none(self):
        assert prod_signs([]) is None

    def test_with_zero_returns_int(self):
        assert isinstance(prod_signs([0, 1]), int)

    def test_negative_result_is_int(self):
        assert isinstance(prod_signs([-1]), int)


class TestSpecificDocstringExamples:
    """Directly verify the examples from the docstring."""

    def test_example_1(self):
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_example_2(self):
        assert prod_signs([0, 1]) == 0

    def test_example_3(self):
        assert prod_signs([]) is None
