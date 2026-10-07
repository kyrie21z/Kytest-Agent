import pytest
from solution import max_product


class TestMaxProductBasic:
    """Test basic functionality of max_product."""

    def test_single_element(self):
        assert max_product([5]) == 5

    def test_two_elements_increasing(self):
        assert max_product([2, 3]) == 6

    def test_two_elements_decreasing(self):
        assert max_product([3, 2]) == 3

    def test_three_elements_increasing(self):
        assert max_product([1, 2, 3]) == 6

    def test_three_elements_with_peak(self):
        # Increasing subseq [1, 2, 4] -> prod 8; [1, 3, 4] not contiguous increasing
        assert max_product([1, 2, 4]) == 8

    def test_all_same_elements(self):
        assert max_product([3, 3, 3]) == 27


class TestMaxProductEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_array(self):
        with pytest.raises(ValueError):
            max_product([])

    def test_negative_numbers_only(self):
        # [-3,-2,-1]: i=0: prod=-3, then (-3)*(-2)=6, then 6*(-1)=-6 => mpis=[-3,6,-6]
        # i=1: prod=-2, then (-2)*(-1)=2 => mpis[2]=max(-6,2)=2
        # i=2: prod=-1
        # mpis=[-3,6,2], max=6
        assert max_product([-3, -2, -1]) == 6

    def test_mixed_positive_and_negative(self):
        # [-5,-3,0,2,5]: i=0: prod=-5, then (-5)*(-3)=15, then 15*0=0, then 0*2=0, then 0*5=0
        # mpis[1]=15, rest 0 from i=0
        # Best single product segment: [-5,-3] gives 15
        assert max_product([-5, -3, 0, 2, 5]) == 15

    def test_zeros_in_array(self):
        # [0, 1, 2] -> prod 0*1*2 = 0; but single element 2 -> 2
        assert max_product([0, 1, 2]) == 2

    def test_large_values(self):
        result = max_product([10, 20, 30])
        assert result == 6000

    def test_one_element_array(self):
        assert max_product([42]) == 42


class TestMaxProductIncreasingSubsequences:
    """Test various increasing subsequence scenarios."""

    def test_longest_increasing_subsequence(self):
        # [1, 2, 3, 4, 5] -> full product = 120
        assert max_product([1, 2, 3, 4, 5]) == 120

    def test_increasing_then_decreasing(self):
        # [1, 2, 3, 2, 1] -> best is [1,2,3] -> prod 6
        assert max_product([1, 2, 3, 2, 1]) == 6

    def test_multiple_increasing_segments(self):
        # [3, 1, 2, 4, 1, 5] -> [1,2,4]=8 or [1,5]=5 or [3]=3 -> max=8
        assert max_product([3, 1, 2, 4, 1, 5]) == 8

    def test_strictly_decreasing(self):
        # [5, 4, 3, 2, 1] -> best single element = 5
        assert max_product([5, 4, 3, 2, 1]) == 5

    def test_alternating_pattern(self):
        # [1, 3, 2, 4, 3, 5] -> [1,3]=3, [2,4]=8, [3,5]=15
        # max = 15
        assert max_product([1, 3, 2, 4, 3, 5]) == 15

    def test_equal_consecutive_elements(self):
        # [2, 2, 3] -> [2,2,3] since 2<=2<=3 -> prod 12
        assert max_product([2, 2, 3]) == 12

    def test_equal_elements_throughout(self):
        # [4, 4, 4] -> all equal, so non-decreasing -> prod 64
        assert max_product([4, 4, 4]) == 64


class TestMaxProductReturnTypes:
    """Test that return types are correct."""

    def test_returns_integer(self):
        assert isinstance(max_product([1, 2, 3]), int)

    def test_returns_correct_type_for_large_input(self):
        result = max_product([10, 10, 10, 10, 10])
        assert isinstance(result, int)
        assert result == 100000


class TestMaxProductSpecificScenarios:
    """Test specific real-world-like scenarios."""

    def test_stock_price_max_product(self):
        # Simulating stock prices where we want max product of rising days
        assert max_product([10, 15, 20, 5, 10, 15]) == 3000  # [10,15,20]

    def test_temperature_rising_sequence(self):
        # Temperature readings over days: 20*21*22*23 = 212520
        assert max_product([20, 21, 22, 23]) == 212520

    def test_single_peak_array(self):
        # [1, 5, 3, 7, 9] -> [1,5]=5, [3,7,9]=189, [1,5,3,7,9] breaks at 5>3
        assert max_product([1, 5, 3, 7, 9]) == 189

    def test_worst_case_single_elements(self):
        # All decreasing, so max is just the largest single element
        assert max_product([9, 8, 7, 6, 5, 4, 3, 2, 1]) == 9

    def test_best_starting_from_first(self):
        assert max_product([2, 4, 6, 8]) == 384
