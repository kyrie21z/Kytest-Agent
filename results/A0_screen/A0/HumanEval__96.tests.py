import pytest
from solution import count_up_to


class TestCountUpTo:
    """Tests for the count_up_to function."""

    # --- Docstring examples ---

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

    def test_zero_returns_empty(self):
        """Zero should return an empty list since there are no primes < 0."""
        assert count_up_to(0) == []

    def test_one_returns_empty(self):
        """One should return an empty list since there are no primes < 1."""
        assert count_up_to(1) == []

    def test_two_returns_empty(self):
        """Two should return an empty list since there are no primes < 2."""
        assert count_up_to(2) == []

    def test_three_returns_single_prime(self):
        """Three should return [2] since 2 is the only prime < 3."""
        assert count_up_to(3) == [2]

    def test_four_returns_two_primes(self):
        """Four should return [2, 3]."""
        assert count_up_to(4) == [2, 3]

    # --- Larger inputs ---

    def test_hundred(self):
        primes_less_than_100 = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,
        ]
        assert count_up_to(100) == primes_less_than_100

    def test_five_hundred(self):
        result = count_up_to(500)
        # Verify all returned values are actually prime and < 500
        assert all(x < 500 for x in result)
        assert len(result) == 95  # There are 95 primes less than 500

    def test_thousand(self):
        result = count_up_to(1000)
        assert all(x < 1000 for x in result)
        assert len(result) == 168  # There are 168 primes less than 1000

    # --- Return type checks ---

    def test_returns_list(self):
        """Ensure the function returns a list."""
        result = count_up_to(10)
        assert isinstance(result, list)

    def test_returns_integers(self):
        """Ensure all elements in the returned list are integers."""
        result = count_up_to(50)
        assert all(isinstance(x, int) for x in result)

    # --- Ordering and uniqueness ---

    def test_result_is_sorted(self):
        """The result should be in ascending order."""
        result = count_up_to(200)
        assert result == sorted(result)

    def test_no_duplicates(self):
        """The result should contain no duplicate values."""
        result = count_up_to(500)
        assert len(result) == len(set(result))

    # --- Prime verification ---

    def test_all_elements_are_prime(self):
        """Every element in the result must be a prime number."""
        result = count_up_to(300)
        for num in result:
            if num < 2:
                pytest.fail(f"{num} is not prime")
            for i in range(2, int(num**0.5) + 1):
                assert num % i != 0, f"{num} is not prime"

    def test_includes_all_primes_below_n(self):
        """All primes below n must be included in the result."""
        n = 100
        expected = [i for i in range(2, n) if all(i % d != 0 for d in range(2, int(i**0.5) + 1))]
        assert count_up_to(n) == expected

    # --- Boundary between prime and non-prime ---

    def test_boundary_at_prime_number(self):
        """When n itself is prime, it should NOT be included."""
        # 7 is prime; count_up_to(7) should include primes < 7, not 7 itself
        assert count_up_to(7) == [2, 3, 5]

    def test_boundary_at_composite_number(self):
        """When n is composite, primes just below it should be included."""
        # 9 is composite; count_up_to(9) should include primes < 9
        assert count_up_to(9) == [2, 3, 5, 7]
