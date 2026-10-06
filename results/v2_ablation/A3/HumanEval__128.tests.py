import pytest
from solution import prod_signs


class TestProdSignsNormalCases:
    """Test normal cases with typical inputs."""

    def test_example_from_docstring_1(self):
        # [1, 2, 2, -4]: sum(abs)=9, sign_product=-1 => -9
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_example_from_docstring_2(self):
        # [0, 1]: contains 0 => 0
        assert prod_signs([0, 1]) == 0

    def test_all_positive(self):
        # [1, 2, 3]: sum(abs)=6, sign_product=1 => 6
        assert prod_signs([1, 2, 3]) == 6

    def test_all_negative(self):
        # [-1, -2, -3]: sum(abs)=6, sign_product=(-1)^3=-1 => -6
        assert prod_signs([-1, -2, -3]) == -6

    def test_single_positive(self):
        # [5]: sum(abs)=5, sign_product=1 => 5
        assert prod_signs([5]) == 5

    def test_single_negative(self):
        # [-5]: sum(abs)=5, sign_product=-1 => -5
        assert prod_signs([-5]) == -5

    def test_mixed_with_even_negatives(self):
        # [-1, -2]: sum(abs)=3, sign_product=(-1)^2=1 => 3
        assert prod_signs([-1, -2]) == 3

    def test_mixed_with_odd_negatives(self):
        # [-1, -2, -3, -4]: sum(abs)=10, sign_product=(-1)^4=1 => 10
        assert prod_signs([-1, -2, -3, -4]) == 10

    def test_large_magnitudes(self):
        # [100, -200, 300]: sum(abs)=600, sign_product=-1 => -600
        assert prod_signs([100, -200, 300]) == -600

    def test_zeros_in_middle(self):
        # [1, 0, 2]: contains 0 => 0
        assert prod_signs([1, 0, 2]) == 0

    def test_multiple_zeros(self):
        # [0, 0, 0]: contains 0 => 0
        assert prod_signs([0, 0, 0]) == 0

    def test_zero_and_negatives(self):
        # [0, -1, -2]: contains 0 => 0
        assert prod_signs([0, -1, -2]) == 0

    def test_only_zeros(self):
        # [0]: contains 0 => 0
        assert prod_signs([0]) == 0


class TestProdSignsEmptyAndNullCases:
    """Test empty, null, and zero-size inputs."""

    def test_empty_list(self):
        # Empty array => None
        assert prod_signs([]) is None

    def test_none_input_raises(self):
        # Passing None should raise TypeError (not documented to handle None)
        with pytest.raises(TypeError):
            prod_signs(None)


class TestProdSignsInvalidInputs:
    """Test invalid input types."""

    def test_string_input_raises(self):
        with pytest.raises(TypeError):
            prod_signs("not a list")

    def test_non_iterable_raises(self):
        with pytest.raises(TypeError):
            prod_signs(42)

    def test_float_in_list_runs(self):
        # Floats don't have integer division semantics expected by x // abs(x)
        # This will produce unexpected results or raise issues depending on Python version.
        # abs(-1.5) = 1.5, -1.5 // 1.5 = -2.0 (floor division), so sgn *= -2.0
        # This is technically valid Python but semantically wrong for the function.
        # We'll test that it runs without crashing but produces a float result.
        result = prod_signs([1.5, -2.5])
        # sum(abs) = 4.0, sign_product = 1 * (-2.0) = -2.0, result = -8.0
        assert isinstance(result, float)


class TestProdSignsBoundaryCases:
    """Test boundary cases at edges of valid input ranges."""

    def test_single_element_zero(self):
        assert prod_signs([0]) == 0

    def test_two_elements_both_zero(self):
        assert prod_signs([0, 0]) == 0

    def test_alternating_signs(self):
        # [1, -1, 1, -1]: sum(abs)=4, sign_product=1 => 4
        assert prod_signs([1, -1, 1, -1]) == 4

    def test_alternating_signs_odd_length(self):
        # [1, -1, 1]: sum(abs)=3, sign_product=-1 => -3
        assert prod_signs([1, -1, 1]) == -3

    def test_largest_common_integers(self):
        # Using small large-ish numbers to avoid overflow concerns
        # [2147483647, -2147483647]: sum(abs)=4294967294, sign_product=-1
        assert prod_signs([2147483647, -2147483647]) == -4294967294

    def test_many_same_value(self):
        # [1]*100: sum(abs)=100, sign_product=1 => 100
        assert prod_signs([1] * 100) == 100

    def test_many_negative_same_value(self):
        # [-1]*100: sum(abs)=100, sign_product=1 (even count) => 100
        assert prod_signs([-1] * 100) == 100

    def test_many_negative_same_value_odd_count(self):
        # [-1]*99: sum(abs)=99, sign_product=-1 (odd count) => -99
        assert prod_signs([-1] * 99) == -99
