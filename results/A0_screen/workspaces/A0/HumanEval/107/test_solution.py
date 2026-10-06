import pytest
from solution import even_odd_palindrome


class TestEvenOddPalindrome:
    """Tests for the even_odd_palindrome function."""

    # ------------------------------------------------------------------
    # Docstring examples
    # ------------------------------------------------------------------

    def test_example_1(self):
        """Example 1 from the docstring: n=3 → (1, 2)."""
        assert even_odd_palindrome(3) == (1, 2)

    def test_example_2(self):
        """Example 2 from the docstring: n=12 → (4, 6)."""
        assert even_odd_palindrome(12) == (4, 6)

    # ------------------------------------------------------------------
    # Edge case: smallest valid input
    # ------------------------------------------------------------------

    def test_single_digit_n_equals_1(self):
        """n=1: only palindrome is 1 (odd)."""
        assert even_odd_palindrome(1) == (0, 1)

    def test_single_digit_n_equals_9(self):
        """n=9: palindromes are 1..9 → 4 even, 5 odd."""
        assert even_odd_palindrome(9) == (4, 5)

    # ------------------------------------------------------------------
    # Two-digit palindromes
    # ------------------------------------------------------------------

    def test_two_digit_palindromes(self):
        """n=11: palindromes are 1..9, 11 → 4 even, 6 odd."""
        assert even_odd_palindrome(11) == (4, 6)

    def test_n_includes_22(self):
        """n=22: adds palindrome 22 (even)."""
        # Palindromes up to 22: 1-9, 11, 22
        # Even: 2, 4, 6, 8, 22 → 5
        # Odd:  1, 3, 5, 7, 9, 11 → 6
        assert even_odd_palindrome(22) == (5, 6)

    # ------------------------------------------------------------------
    # Three-digit palindromes
    # ------------------------------------------------------------------

    def test_three_digit_palindromes(self):
        """n=100: includes 101 (odd palindrome)."""
        result = even_odd_palindrome(100)
        # Verify return type
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_n_equals_101(self):
        """n=101: adds palindrome 101 (odd)."""
        result = even_odd_palindrome(101)
        assert isinstance(result, tuple)
        assert len(result) == 2

    # ------------------------------------------------------------------
    # Return value properties
    # ------------------------------------------------------------------

    def test_returns_tuple(self):
        """The function should always return a tuple."""
        result = even_odd_palindrome(5)
        assert isinstance(result, tuple)

    def test_returns_two_elements(self):
        """The returned tuple must have exactly two elements."""
        result = even_odd_palindrome(5)
        assert len(result) == 2

    def test_both_counts_non_negative(self):
        """Both even and odd counts should be >= 0."""
        for n in [1, 5, 10, 50, 100]:
            even, odd = even_odd_palindrome(n)
            assert even >= 0
            assert odd >= 0

    def test_sum_matches_total_palindromes(self):
        """even + odd should equal total number of palindromes in [1, n]."""
        def count_palindromes(n):
            return sum(1 for i in range(1, n + 1) if str(i) == str(i)[::-1])

        for n in [1, 5, 10, 20, 50, 100, 500, 1000]:
            even, odd = even_odd_palindrome(n)
            assert even + odd == count_palindromes(n)

    # ------------------------------------------------------------------
    # Monotonicity / incremental checks
    # ------------------------------------------------------------------

    def test_even_count_never_decreases(self):
        """As n increases, the even count should never decrease."""
        prev_even = -1
        for n in range(1, 101):
            even, _ = even_odd_palindrome(n)
            assert even >= prev_even
            prev_even = even

    def test_odd_count_never_decreases(self):
        """As n increases, the odd count should never decrease."""
        prev_odd = -1
        for n in range(1, 101):
            _, odd = even_odd_palindrome(n)
            assert odd >= prev_odd
            prev_odd = odd

    # ------------------------------------------------------------------
    # Specific known values
    # ------------------------------------------------------------------

    def test_n_equals_5(self):
        """n=5: palindromes 1,2,3,4,5 → 2 even, 3 odd."""
        assert even_odd_palindrome(5) == (2, 3)

    def test_n_equals_10(self):
        """n=10: palindromes 1..9 → 4 even, 5 odd."""
        assert even_odd_palindrome(10) == (4, 5)

    def test_n_equals_1000(self):
        """n=1000: max documented input."""
        result = even_odd_palindrome(1000)
        assert isinstance(result, tuple)
        assert len(result) == 2
        even, odd = result
        assert even >= 0
        assert odd >= 0

    # ------------------------------------------------------------------
    # Type checking
    # ------------------------------------------------------------------

    def test_return_type_integers(self):
        """Both elements of the returned tuple should be integers."""
        even, odd = even_odd_palindrome(50)
        assert isinstance(even, int)
        assert isinstance(odd, int)

    # ------------------------------------------------------------------
    # Non-palindrome numbers don't affect counts
    # ------------------------------------------------------------------

    def test_range_without_new_palindromes(self):
        """Between consecutive palindromes, counts stay the same."""
        # 10 and 11: 10 is not a palindrome, so counts at 10 == counts at 9
        assert even_odd_palindrome(10) == even_odd_palindrome(9)
        # 12 and 13: neither is a palindrome
        assert even_odd_palindrome(12) == even_odd_palindrome(13)
