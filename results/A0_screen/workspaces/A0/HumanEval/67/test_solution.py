import pytest
from solution import fruit_distribution


class TestFruitDistributionBasic:
    """Test basic functionality with examples from docstring."""

    def test_example_1(self):
        assert fruit_distribution("5 apples and 6 oranges", 19) == 8

    def test_example_2(self):
        assert fruit_distribution("0 apples and 1 oranges", 3) == 2

    def test_example_3(self):
        assert fruit_distribution("2 apples and 3 oranges", 100) == 95

    def test_example_4(self):
        assert fruit_distribution("100 apples and 1 oranges", 120) == 19


class TestFruitDistributionEdgeCases:
    """Test edge cases."""

    def test_zero_apples_and_zero_oranges(self):
        # All fruits are mangoes
        assert fruit_distribution("0 apples and 0 oranges", 10) == 10

    def test_all_apples_no_oranges(self):
        assert fruit_distribution("10 apples and 0 oranges", 15) == 5

    def test_no_apples_all_oranges(self):
        assert fruit_distribution("0 apples and 10 oranges", 15) == 5

    def test_all_mangoes(self):
        assert fruit_distribution("0 apples and 0 oranges", 0) == 0

    def test_single_mango(self):
        assert fruit_distribution("0 apples and 0 oranges", 1) == 1

    def test_one_apple_one_orange(self):
        assert fruit_distribution("1 apples and 1 oranges", 5) == 3


class TestFruitDistributionLargeNumbers:
    """Test with large input values."""

    def test_large_numbers(self):
        assert fruit_distribution("1000 apples and 2000 oranges", 5000) == 2000

    def test_very_large_total(self):
        assert fruit_distribution("1 apples and 2 oranges", 1000000) == 999997


class TestFruitDistributionInvalidInputs:
    """Test invalid inputs that violate the contract."""

    def test_negative_result_raises_assertion(self):
        # Total fruits is less than sum of apples and oranges
        with pytest.raises(AssertionError, match="invalid inputs"):
            fruit_distribution("10 apples and 20 oranges", 15)

    def test_equal_sum_exceeds_total(self):
        with pytest.raises(AssertionError, match="invalid inputs"):
            fruit_distribution("5 apples and 5 oranges", 9)

    def test_zero_total_with_fruits(self):
        with pytest.raises(AssertionError, match="invalid inputs"):
            fruit_distribution("1 apples and 1 oranges", 0)


class TestFruitDistributionStringFormats:
    """Test various string parsing scenarios."""

    def test_single_digit_numbers(self):
        assert fruit_distribution("1 apples and 2 oranges", 10) == 7

    def test_double_digit_numbers(self):
        assert fruit_distribution("12 apples and 34 oranges", 100) == 54

    def test_three_digit_numbers(self):
        assert fruit_distribution("100 apples and 200 oranges", 500) == 200

    def test_mixed_digit_lengths(self):
        assert fruit_distribution("1 apples and 99 oranges", 200) == 100
