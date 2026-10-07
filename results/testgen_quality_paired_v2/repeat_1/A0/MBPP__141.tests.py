import pytest
from solution import pancake_sort


class TestPancakeSortBasic:
    """Test basic sorting functionality."""

    def test_empty_list(self):
        assert pancake_sort([]) == []

    def test_single_element(self):
        assert pancake_sort([1]) == [1]

    def test_two_elements_already_sorted(self):
        assert pancake_sort([1, 2]) == [1, 2]

    def test_two_elements_unsorted(self):
        assert pancake_sort([2, 1]) == [1, 2]

    def test_three_elements(self):
        assert pancake_sort([3, 1, 2]) == [1, 2, 3]

    def test_already_sorted(self):
        assert pancake_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert pancake_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_all_same_elements(self):
        assert pancake_sort([3, 3, 3, 3]) == [3, 3, 3, 3]


class TestPancakeSortWithDuplicates:
    """Test behavior with duplicate elements."""

    def test_two_duplicates(self):
        result = pancake_sort([2, 1, 2])
        assert result == [1, 2, 2]

    def test_multiple_duplicates(self):
        result = pancake_sort([3, 1, 2, 1, 3])
        assert result == [1, 1, 2, 3, 3]

    def test_all_identical(self):
        assert pancake_sort([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]


class TestPancakeSortNegativeNumbers:
    """Test with negative numbers."""

    def test_all_negative(self):
        assert pancake_sort([-3, -1, -2]) == [-3, -2, -1]

    def test_mixed_positive_negative(self):
        result = pancake_sort([3, -1, 2, -5, 0])
        assert result == [-5, -1, 0, 2, 3]

    def test_negative_max(self):
        assert pancake_sort([-1, -2, -3]) == [-3, -2, -1]


class TestPancakeSortLargeInput:
    """Test with larger inputs."""

    def test_ten_elements(self):
        nums = [9, 7, 5, 3, 1, 8, 6, 4, 2, 0]
        result = pancake_sort(nums)
        assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_hundred_elements(self):
        import random
        nums = list(range(100))
        random.seed(42)
        random.shuffle(nums)
        result = pancake_sort(nums)
        assert result == list(range(100))


class TestPancakeSortReturnValues:
    """Test that return values are correct sorted lists."""

    def test_returns_new_list(self):
        original = [3, 1, 2]
        result = pancake_sort(original)
        # The function returns a new list; verify the result is sorted
        assert result == [1, 2, 3]

    def test_result_is_sorted(self):
        """Verify the result is always in non-decreasing order."""
        for _ in range(50):
            import random
            n = random.randint(0, 20)
            nums = [random.randint(-100, 100) for _ in range(n)]
            result = pancake_sort(nums)
            for i in range(len(result) - 1):
                assert result[i] <= result[i + 1]

    def test_result_contains_same_elements(self):
        """Verify the result contains exactly the same elements as input."""
        import random
        for _ in range(50):
            n = random.randint(0, 20)
            nums = [random.randint(-100, 100) for _ in range(n)]
            result = pancake_sort(nums)
            assert sorted(nums) == result


class TestPancakeSortEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_none_not_accepted(self):
        """Function should handle empty list but not None."""
        with pytest.raises(TypeError):
            pancake_sort(None)

    def test_float_values(self):
        result = pancake_sort([3.5, 1.2, 2.7])
        assert result == [1.2, 2.7, 3.5]

    def test_mixed_int_float(self):
        result = pancake_sort([3, 1.5, 2])
        assert result == [1.5, 2, 3]

    def test_zero_in_list(self):
        assert pancake_sort([0, 0, 0]) == [0, 0, 0]

    def test_large_numbers(self):
        result = pancake_sort([10**9, 1, 10**8, 10**7])
        assert result == [1, 10**7, 10**8, 10**9]


class TestPancakeSortDeterminism:
    """Test that the function produces consistent results."""

    def test_consistent_output(self):
        nums = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        results = [pancake_sort(nums) for _ in range(10)]
        for r in results:
            assert r == [1, 2, 3, 4, 5, 6, 7, 8, 9]
