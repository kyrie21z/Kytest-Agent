import pytest
from solution import sum_div


class TestSumDivBasic:
    """Test basic functionality of sum_div."""

    def test_small_prime(self):
        # Prime numbers have only 1 as a proper divisor
        assert sum_div(2) == 1
        assert sum_div(3) == 1
        assert sum_div(5) == 1
        assert sum_div(7) == 1
        assert sum_div(11) == 1

    def test_perfect_number(self):
        # 6 is a perfect number: divisors are 1, 2, 3 -> sum = 6
        assert sum_div(6) == 6

    def test_non_perfect_number(self):
        # 12: divisors are 1, 2, 3, 4, 6 -> sum = 16
        assert sum_div(12) == 16
        # 10: divisors are 1, 2, 5 -> sum = 8
        assert sum_div(10) == 8
        # 9: divisors are 1, 3 -> sum = 4
        assert sum_div(9) == 4

    def test_larger_numbers(self):
        # 28 is a perfect number: divisors 1, 2, 4, 7, 14 -> sum = 28
        assert sum_div(28) == 28
        # 16: divisors 1, 2, 4, 8 -> sum = 15
        assert sum_div(16) == 15
        # 30: divisors 1, 2, 3, 5, 6, 10, 15 -> sum = 42
        assert sum_div(30) == 42


class TestSumDivEdgeCases:
    """Test edge cases of sum_div."""

    def test_zero(self):
        # 0: the function returns 1 (only [1] in the list)
        # This reflects the actual implementation behavior
        assert sum_div(0) == 1

    def test_one(self):
        # 1: the function returns 1 (only [1] in the list)
        assert sum_div(1) == 1

    def test_negative_numbers(self):
        # Negative numbers: range(2, negative) is empty, returns 1
        assert sum_div(-1) == 1
        assert sum_div(-5) == 1

    def test_large_number(self):
        # 100: divisors 1, 2, 4, 5, 10, 20, 25, 50 -> sum = 117
        assert sum_div(100) == 117
        # 496 is a perfect number
        assert sum_div(496) == 496


class TestSumDivReturnTypes:
    """Test return types of sum_div."""

    def test_returns_integer(self):
        assert isinstance(sum_div(6), int)
        assert isinstance(sum_div(12), int)
        assert isinstance(sum_div(100), int)


class TestSumDivDivisorCorrectness:
    """Verify that all returned divisors actually divide the number."""

    def test_all_divisors_are_valid(self):
        """For each number tested, verify every divisor divides it evenly."""
        for n in range(2, 100):
            result = sum_div(n)
            # Reconstruct divisors to verify correctness
            divisors = [1]
            for i in range(2, n):
                if n % i == 0:
                    divisors.append(i)
            assert result == sum(divisors), f"Failed for {n}"
