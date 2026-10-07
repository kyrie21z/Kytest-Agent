from solution import is_Monotonic


class TestIsMonotonic:
    """Tests for the is_Monotonic function."""

    def test_empty_list(self):
        assert is_Monotonic([]) is True

    def test_single_element(self):
        assert is_Monotonic([1]) is True

    def test_two_equal_elements(self):
        assert is_Monotonic([3, 3]) is True

    def test_two_increasing(self):
        assert is_Monotonic([1, 2]) is True

    def test_two_decreasing(self):
        assert is_Monotonic([2, 1]) is True

    def test_strictly_increasing(self):
        assert is_Monotonic([1, 2, 3, 4, 5]) is True

    def test_strictly_decreasing(self):
        assert is_Monotonic([5, 4, 3, 2, 1]) is True

    def test_constant_array(self):
        assert is_Monotonic([7, 7, 7, 7]) is True

    def test_non_monotonic_up_then_down(self):
        assert is_Monotonic([1, 3, 2]) is False

    def test_non_monotonic_down_then_up(self):
        assert is_Monotonic([5, 3, 4]) is False

    def test_non_monotonic_v_shape(self):
        assert is_Monotonic([3, 1, 2]) is False

    def test_with_duplicates_increasing(self):
        assert is_Monotonic([1, 2, 2, 3]) is True

    def test_with_duplicates_decreasing(self):
        assert is_Monotonic([4, 2, 2, 0]) is True

    def test_negative_numbers_increasing(self):
        assert is_Monotonic([-5, -3, -1, 0]) is True

    def test_negative_numbers_decreasing(self):
        assert is_Monotonic([0, -1, -3, -5]) is True

    def test_mixed_positive_negative_not_monotonic(self):
        assert is_Monotonic([-1, 0, -1, 0]) is False

    def test_all_zeros(self):
        assert is_Monotonic([0, 0, 0, 0, 0]) is True

    def test_large_increasing(self):
        assert is_Monotonic(list(range(100))) is True

    def test_large_decreasing(self):
        assert is_Monotonic(list(range(100, 0, -1))) is True

    def test_float_increasing(self):
        assert is_Monotonic([1.1, 2.2, 3.3]) is True

    def test_float_decreasing(self):
        assert is_Monotonic([3.3, 2.2, 1.1]) is True

    def test_float_not_monotonic(self):
        assert is_Monotonic([1.0, 2.0, 1.5]) is False
