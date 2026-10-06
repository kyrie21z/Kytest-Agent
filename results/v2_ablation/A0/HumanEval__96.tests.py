import pytest
from solution import count_up_to


class TestCountUpTo:
    """Tests for the count_up_to function."""

    def test_zero(self):
        """When n is 0, no primes less than 0 exist."""
        assert count_up_to(0) == []

    def test_one(self):
        """When n is 1, no primes less than 1 exist."""
        assert count_up_to(1) == []

    def test_two(self):
        """When n is 2, no primes strictly less than 2 exist."""
        assert count_up_to(2) == []

    def test_three(self):
        """When n is 3, only prime less than 3 is [2]."""
        assert count_up_to(3) == [2]

    def test_five(self):
        """Primes less than 5 are [2, 3]."""
        assert count_up_to(5) == [2, 3]

    def test_eleven(self):
        """Primes less than 11 are [2, 3, 5, 7]."""
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_twenty(self):
        """Primes less than 20 are [2, 3, 5, 7, 11, 13, 17, 19]."""
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_eighteen(self):
        """Primes less than 18 are [2, 3, 5, 7, 11, 13, 17]."""
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]

    def test_prime_boundary(self):
        """When n itself is prime, it should NOT be included."""
        # 7 is prime; primes less than 7 are [2, 3, 5]
        assert count_up_to(7) == [2, 3, 5]

    def test_larger_number(self):
        """Test with a larger value to ensure correctness at scale."""
        assert count_up_to(50) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    def test_returns_list(self):
        """Ensure the return type is always a list."""
        assert isinstance(count_up_to(10), list)

    def test_all_elements_are_integers(self):
        """Ensure all returned elements are integers."""
        result = count_up_to(30)
        assert all(isinstance(x, int) for x in result)

    def test_result_is_sorted(self):
        """Ensure the returned list is sorted in ascending order."""
        result = count_up_to(100)
        assert result == sorted(result)

    def test_no_duplicates(self):
        """Ensure there are no duplicate values in the result."""
        result = count_up_to(50)
        assert len(result) == len(set(result))

    def test_empty_for_small_n(self):
        """For n <= 2, the result should be empty."""
        for n in range(0, 3):
            assert count_up_to(n) == []
