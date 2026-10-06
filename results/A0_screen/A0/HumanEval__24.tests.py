import pytest
from solution import largest_divisor


class TestLargestDivisor:
    """Tests for the largest_divisor function."""

    # --- Docstring example ---
    def test_docstring_example(self):
        assert largest_divisor(15) == 5

    # --- Basic composite numbers ---
    def test_even_number(self):
        assert largest_divisor(10) == 5

    def test_multiple_of_three(self):
        assert largest_divisor(21) == 7

    def test_multiple_of_five(self):
        assert largest_divisor(25) == 5

    def test_hundred(self):
        assert largest_divisor(100) == 50

    def test_two_hundred(self):
        assert largest_divisor(200) == 100

    # --- Prime numbers (should return 1) ---
    def test_prime_2(self):
        assert largest_divisor(2) == 1

    def test_prime_3(self):
        assert largest_divisor(3) == 1

    def test_prime_7(self):
        assert largest_divisor(7) == 1

    def test_prime_13(self):
        assert largest_divisor(13) == 1

    def test_prime_97(self):
        assert largest_divisor(97) == 1

    # --- Perfect squares ---
    def test_perfect_square_4(self):
        assert largest_divisor(4) == 2

    def test_perfect_square_9(self):
        assert largest_divisor(9) == 3

    def test_perfect_square_16(self):
        assert largest_divisor(16) == 8

    def test_perfect_square_25(self):
        assert largest_divisor(25) == 5

    def test_perfect_square_49(self):
        assert largest_divisor(49) == 7

    # --- Edge case: n=1 ---
    def test_one(self):
        assert largest_divisor(1) == 1

    # --- Larger numbers ---
    def test_large_composite(self):
        assert largest_divisor(1000) == 500

    def test_larger_prime(self):
        assert largest_divisor(101) == 1

    def test_product_of_two_primes(self):
        # 6 = 2 * 3, largest proper divisor is 3
        assert largest_divisor(6) == 3

    def test_product_of_three_primes(self):
        # 30 = 2 * 3 * 5, largest proper divisor is 15
        assert largest_divisor(30) == 15

    # --- Type and value checks ---
    def test_returns_integer(self):
        result = largest_divisor(12)
        assert isinstance(result, int)

    def test_result_is_proper_divisor(self):
        """The result must divide n evenly and be less than n."""
        for n in [4, 6, 8, 9, 10, 12, 15, 16, 20, 24, 30]:
            result = largest_divisor(n)
            assert n % result == 0
            assert result < n

    def test_result_is_largest_proper_divisor(self):
        """Verify the returned divisor is indeed the largest one."""
        for n in range(2, 101):
            expected = max(d for d in range(1, n) if n % d == 0)
            assert largest_divisor(n) == expected
