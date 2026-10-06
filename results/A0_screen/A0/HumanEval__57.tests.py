import pytest
from solution import monotonic


# --- Monotonically Increasing ---

class TestMonotonicallyIncreasing:
    def test_simple_increasing(self):
        assert monotonic([1, 2, 4, 20]) is True

    def test_single_element(self):
        assert monotonic([5]) is True

    def test_two_elements_increasing(self):
        assert monotonic([1, 2]) is True

    def test_all_same_elements(self):
        assert monotonic([3, 3, 3, 3]) is True

    def test_two_same_elements(self):
        assert monotonic([7, 7]) is True

    def test_increasing_with_negatives(self):
        assert monotonic([-3, -2, -1, 0]) is True

    def test_increasing_with_mixed_signs(self):
        assert monotonic([-5, -1, 0, 3, 7]) is True

    def test_large_increasing_list(self):
        assert monotonic(list(range(1000))) is True


# --- Monotonically Decreasing ---

class TestMonotonicallyDecreasing:
    def test_simple_decreasing(self):
        assert monotonic([4, 1, 0, -10]) is True

    def test_two_elements_decreasing(self):
        assert monotonic([10, 5]) is True

    def test_decreasing_with_positives(self):
        assert monotonic([100, 50, 25, 10]) is True

    def test_decreasing_with_mixed_signs(self):
        assert monotonic([5, 1, 0, -3, -8]) is True

    def test_large_decreasing_list(self):
        assert monotonic(list(range(1000, 0, -1))) is True


# --- Not Monotonic ---

class TestNotMonotonic:
    def test_simple_not_monotonic(self):
        assert monotonic([1, 20, 4, 10]) is False

    def test_v_shape(self):
        assert monotonic([1, 3, 2]) is False

    def test_inverted_v_shape(self):
        assert monotonic([3, 1, 2]) is False

    def test_oscillating(self):
        assert monotonic([1, 2, 1, 2, 1]) is False

    def test_constant_then_change(self):
        assert monotonic([1, 1, 2, 1]) is False

    def test_change_then_constant(self):
        assert monotonic([1, 2, 2, 1]) is False

    def test_random_order(self):
        assert monotonic([5, 1, 4, 2, 3]) is False


# --- Edge Cases ---

class TestEdgeCases:
    def test_empty_list(self):
        assert monotonic([]) is True

    def test_single_element_list(self):
        assert monotonic([42]) is True

    def test_two_equal_elements(self):
        assert monotonic([7, 7]) is True

    def test_two_different_elements_increasing(self):
        assert monotonic([1, 99]) is True

    def test_two_different_elements_decreasing(self):
        assert monotonic([99, 1]) is True

    def test_float_values_increasing(self):
        assert monotonic([1.1, 2.2, 3.3]) is True

    def test_float_values_decreasing(self):
        assert monotonic([3.3, 2.2, 1.1]) is True

    def test_float_values_not_monotonic(self):
        assert monotonic([1.0, 2.0, 1.5]) is False

    def test_zero_in_middle(self):
        assert monotonic([5, 0, -5]) is True

    def test_zeros_only(self):
        assert monotonic([0, 0, 0]) is True


# --- Docstring Examples ---

class TestDocstringExamples:
    def test_example_1(self):
        """[1, 2, 4, 20] -> True"""
        assert monotonic([1, 2, 4, 20]) is True

    def test_example_2(self):
        """[1, 20, 4, 10] -> False"""
        assert monotonic([1, 20, 4, 10]) is False

    def test_example_3(self):
        """[4, 1, 0, -10] -> True"""
        assert monotonic([4, 1, 0, -10]) is True
