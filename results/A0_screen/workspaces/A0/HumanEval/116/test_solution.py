import pytest
from solution import sort_array


class TestSortArrayBasic:
    """Test basic sorting functionality."""

    def test_example_ones_count_sort(self):
        # 1(1), 5(2), 2(1), 3(2), 4(1) -> sorted by ones then value
        assert sort_array([1, 5, 2, 3, 4]) == [1, 2, 4, 3, 5]

    def test_with_zero(self):
        # 0(0), 1(1), 2(1), 3(2), 4(1) -> sorted by ones then value
        assert sort_array([1, 0, 2, 3, 4]) == [0, 1, 2, 4, 3]

    def test_single_element(self):
        assert sort_array([42]) == [42]

    def test_empty_array(self):
        assert sort_array([]) == []


class TestSortByOnesCount:
    """Test that sorting is primarily by number of ones in binary."""

    def test_two_elements_different_ones(self):
        # 3 = 0b11 (two ones), 4 = 0b100 (one one)
        assert sort_array([3, 4]) == [4, 3]

    def test_multiple_groups_by_ones_count(self):
        # 1(1), 2(1), 4(1), 3(2), 5(2), 7(3)
        result = sort_array([7, 5, 3, 4, 2, 1])
        assert result == [1, 2, 4, 3, 5, 7]

    def test_power_of_two_vs_larger_number_fewer_ones(self):
        # 8 = 0b1000 (one one), 15 = 0b1111 (four ones)
        assert sort_array([15, 8]) == [8, 15]

    def test_many_ones_vs_few_ones(self):
        # 7 = 0b111 (three ones), 16 = 0b10000 (one one)
        assert sort_array([7, 16]) == [16, 7]


class TestTieBreakingByDecimalValue:
    """Test secondary sort by decimal value when ones count is equal."""

    def test_same_ones_count_sorted_by_value(self):
        # 3(0b11), 5(0b101), 6(0b110) all have two ones
        assert sort_array([6, 3, 5]) == [3, 5, 6]

    def test_all_same_ones_count(self):
        # 1(1), 2(1), 4(1), 8(1), 16(1) all have one one
        assert sort_array([16, 8, 4, 2, 1]) == [1, 2, 4, 8, 16]

    def test_mixed_same_ones_count(self):
        # 1(1), 2(1), 4(1), 3(2), 5(2), 6(2)
        result = sort_array([6, 5, 3, 4, 2, 1])
        assert result == [1, 2, 4, 3, 5, 6]

    def test_duplicate_values(self):
        # Duplicates should remain in stable positions
        assert sort_array([3, 3, 5, 5]) == [3, 3, 5, 5]

    def test_zeros_and_ones(self):
        # 0(0 ones), 1(1 one), 2(1 one), 4(1 one)
        assert sort_array([4, 2, 1, 0]) == [0, 1, 2, 4]


class TestLargerNumbers:
    """Test with larger integer values."""

    def test_large_numbers(self):
        # 255 = 0b11111111 (8 ones), 256 = 0b100000000 (one one)
        assert sort_array([255, 256]) == [256, 255]

    def test_various_large_numbers(self):
        result = sort_array([1023, 512, 1024, 1])
        # 1023 = 0b1111111111 (10 ones), 512 = 0b1000000000 (1 one)
        # 1024 = 0b10000000000 (1 one), 1 = 0b1 (1 one)
        assert result == [1, 512, 1024, 1023]

    def test_max_common_range(self):
        # Numbers up to 100
        arr = list(range(1, 101))
        result = sort_array(arr)
        # Verify each adjacent pair satisfies the ordering constraint
        for i in range(len(result) - 1):
            x_ones = bin(result[i]).count('1')
            y_ones = bin(result[i + 1]).count('1')
            if x_ones == y_ones:
                assert result[i] <= result[i + 1]
            else:
                assert x_ones < y_ones


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_all_zeros(self):
        assert sort_array([0, 0, 0]) == [0, 0, 0]

    def test_all_ones(self):
        assert sort_array([1, 1, 1]) == [1, 1, 1]

    def test_already_sorted_but_not_by_ones(self):
        # 0(0), 1(1), 2(1), 3(2), 4(1), 5(2), 6(2), 7(3)
        # Correct order: [0, 1, 2, 4, 3, 5, 6, 7]
        result = sort_array([0, 1, 2, 3, 4, 5, 6, 7])
        assert result == [0, 1, 2, 4, 3, 5, 6, 7]

    def test_reverse_sorted(self):
        # 7(3), 6(2), 5(2), 4(1), 3(2), 2(1), 1(1), 0(0)
        result = sort_array([7, 6, 5, 4, 3, 2, 1, 0])
        expected = [0, 1, 2, 4, 3, 5, 6, 7]
        assert result == expected

    def test_two_identical_elements(self):
        assert sort_array([5, 5]) == [5, 5]

    def test_alternating_pattern(self):
        result = sort_array([10, 5, 3, 1, 8, 7])
        # 10=0b1010(2), 5=0b101(2), 3=0b11(2), 1=0b1(1), 8=0b1000(1), 7=0b111(3)
        expected = [1, 8, 3, 5, 10, 7]
        assert result == expected


class TestReturnValueType:
    """Test that return type is correct."""

    def test_returns_list(self):
        assert isinstance(sort_array([1, 2, 3]), list)

    def test_does_not_mutate_input(self):
        original = [3, 1, 2]
        original_copy = original[:]
        sort_array(original)
        assert original == original_copy
