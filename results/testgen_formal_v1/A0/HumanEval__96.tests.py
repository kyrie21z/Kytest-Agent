import pytest
from solution import count_up_to


class TestCountUpTo:
    """Tests for the count_up_to function."""

    # --- Documented examples ---

    def test_count_up_to_5(self):
        assert count_up_to(5) == [2, 3]

    def test_count_up_to_11(self):
        assert count_up_to(11) == [2, 3, 5, 7]

    def test_count_up_to_0(self):
        assert count_up_to(0) == []

    def test_count_up_to_20(self):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_count_up_to_1(self):
        assert count_up_to(1) == []

    def test_count_up_to_18(self):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]

    # --- Edge cases ---

    def test_count_up_to_2(self):
        """No primes strictly less than 2."""
        assert count_up_to(2) == []

    def test_count_up_to_3(self):
        """Only prime less than 3 is 2."""
        assert count_up_to(3) == [2]

    def test_count_up_to_large(self):
        """Test with a larger value to ensure correctness at scale."""
        assert count_up_to(100) == [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]

    def test_count_up_to_prime_boundary(self):
        """When n itself is prime, it should NOT be included (strictly less than n)."""
        assert count_up_to(7) == [2, 3, 5]

    def test_count_up_to_composite_boundary(self):
        """When n is composite, primes up to n-1 should be returned."""
        assert count_up_to(10) == [2, 3, 5, 7]

    # --- Type / input validation ---

    def test_returns_list(self):
        """Ensure the return type is always a list."""
        assert isinstance(count_up_to(10), list)

    def test_all_elements_are_integers(self):
        """Every element in the result must be an integer."""
        result = count_up_to(30)
        assert all(isinstance(x, int) for x in result)

    def test_results_are_sorted(self):
        """Results should be in ascending order."""
        result = count_up_to(50)
        assert result == sorted(result)

    def test_no_duplicates(self):
        """There should be no duplicate primes in the result."""
        result = count_up_to(100)
        assert len(result) == len(set(result))

    def test_all_results_are_prime(self):
        """Every returned number must actually be prime."""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        for n in [5, 11, 20, 50, 100]:
            result = count_up_to(n)
            assert all(is_prime(x) for x in result), f"Non-prime found in count_up_to({n})"

    def test_all_primes_less_than_n_included(self):
        """Every prime less than n must appear in the result."""
        def get_primes(limit):
            sieve = [True] * limit
            for i in range(2, int(limit ** 0.5) + 1):
                if sieve[i]:
                    for j in range(i * i, limit, i):
                        sieve[j] = False
            return [i for i in range(2, limit) if sieve[i]]

        for n in [5, 11, 20, 50, 100]:
            expected = get_primes(n)
            assert count_up_to(n) == expected
