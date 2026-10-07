import pytest
from solution import prod_signs


class TestProdSignsEmpty:
    """Test cases for empty / null-like inputs."""

    def test_empty_list_returns_none(self):
        assert prod_signs([]) is None


class TestProdSignsWithZero:
    """Cases where the array contains zero — should return 0."""

    def test_single_zero(self):
        assert prod_signs([0]) == 0

    def test_zero_with_positive(self):
        assert prod_signs([0, 1]) == 0

    def test_zero_with_negative(self):
        assert prod_signs([0, -3]) == 0

    def test_multiple_zeros(self):
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_in_middle(self):
        assert prod_signs([2, 0, 3]) == 0


class TestProdSignsAllPositive:
    """All elements are positive — sign product is +1."""

    def test_all_positive(self):
        assert prod_signs([1, 2, 2, 4]) == 9

    def test_single_positive(self):
        assert prod_signs([5]) == 5

    def test_larger_positive_values(self):
        assert prod_signs([10, 20, 30]) == 60

    def test_mixed_positive_integers(self):
        assert prod_signs([3, 5, 7]) == 15


class TestProdSignsAllNegative:
    """All elements are negative — sign product depends on count."""

    def test_two_negatives_even_count(self):
        # [-3, -5]: sum_abs=8, sign_prod=(-1)*(-1)=1 => 8
        assert prod_signs([-3, -5]) == 8

    def test_three_negatives_odd_count(self):
        # [-1, -2, -3]: sum_abs=6, sign_prod=(-1)^3=-1 => -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_single_negative(self):
        assert prod_signs([-5]) == -5

    def test_four_negatives_even_count(self):
        # [-1, -2, -3, -4]: sum_abs=10, sign_prod=1 => 10
        assert prod_signs([-1, -2, -3, -4]) == 10


class TestProdSignsMixedSigns:
    """Arrays with both positive and negative numbers."""

    def test_example_from_docstring(self):
        # [1, 2, 2, -4]: sum_abs=9, sign_prod=-1 => -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_one_negative_others_positive(self):
        # [-3, 5, 7]: sum_abs=15, sign_prod=-1 => -15
        assert prod_signs([-3, 5, 7]) == -15

    def test_two_negatives_others_positive(self):
        # [-1, -2, 3]: sum_abs=6, sign_prod=1 => 6
        assert prod_signs([-1, -2, 3]) == 6

    def test_alternating_signs(self):
        # [1, -1, 1, -1]: sum_abs=4, sign_prod=1 => 4
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_large_positive_with_single_negative(self):
        # [100, -1]: sum_abs=101, sign_prod=-1 => -101
        assert prod_signs([100, -1]) == -101


class TestProdSignsEdgeValues:
    """Boundary values at edges of valid input ranges."""

    def test_minimal_nonzero_element(self):
        # [1]: sum_abs=1, sign_prod=1 => 1
        assert prod_signs([1]) == 1

    def test_maximal_single_element(self):
        # Large single value
        assert prod_signs([1000000]) == 1000000

    def test_large_negative_single_element(self):
        assert prod_signs([-1000000]) == -1000000

    def test_many_ones(self):
        # 10 ones: sum_abs=10, sign_prod=1 => 10
        assert prod_signs([1] * 10) == 10

    def test_many_negative_ones(self):
        # 5 negative ones: sum_abs=5, sign_prod=-1 => -5
        assert prod_signs([-1] * 5) == -5

    def test_many_negative_ones_even_count(self):
        # 6 negative ones: sum_abs=6, sign_prod=1 => 6
        assert prod_signs([-1] * 6) == 6

    def test_mix_of_1_and_minus_1(self):
        # [1, -1, 1]: sum_abs=3, sign_prod=-1 => -3
        assert prod_signs([1, -1, 1]) == -3


class TestProdSignsReturnTypes:
    """Verify correct return types."""

    def test_empty_returns_none_type(self):
        result = prod_signs([])
        assert result is None

    def test_nonempty_returns_int(self):
        assert isinstance(prod_signs([1, -2, 3]), int)

    def test_zero_case_returns_int(self):
        assert isinstance(prod_signs([0, 5]), int)
        assert prod_signs([0, 5]) == 0
