import pytest
from solution import is_prime


class TestIsPrime:
    """Unit tests for the is_prime function."""

    # --- Edge cases ---

    def test_negative_numbers(self):
        """Negative numbers are not prime."""
        assert is_prime(-1) is False
        assert is_prime(-2) is False
        assert is_prime(-100) is False

    def test_zero(self):
        """Zero is not prime."""
        assert is_prime(0) is False

    def test_one(self):
        """One is not prime."""
        assert is_prime(1) is False

    # --- Smallest prime ---

    def test_two(self):
        """Two is the smallest and only even prime."""
        assert is_prime(2) is True

    def test_three(self):
        """Three is prime."""
        assert is_prime(3) is True

    # --- Small primes ---

    def test_small_primes(self):
        """Various small prime numbers."""
        assert is_prime(5) is True
        assert is_prime(7) is True
        assert is_prime(11) is True
        assert is_prime(13) is True
        assert is_prime(17) is True
        assert is_prime(19) is True
        assert is_prime(23) is True

    # --- Small non-primes ---

    def test_small_non_primes(self):
        """Various small composite numbers."""
        assert is_prime(4) is False
        assert is_prime(6) is False
        assert is_prime(8) is False
        assert is_prime(9) is False
        assert is_prime(10) is False
        assert is_prime(12) is False

    # --- Docstring examples ---

    def test_docstring_example_6(self):
        assert is_prime(6) is False

    def test_docstring_example_101(self):
        assert is_prime(101) is True

    def test_docstring_example_11(self):
        assert is_prime(11) is True

    def test_docstring_example_13441(self):
        assert is_prime(13441) is True

    def test_docstring_example_61(self):
        assert is_prime(61) is True

    def test_docstring_example_4(self):
        assert is_prime(4) is False

    def test_docstring_example_1(self):
        assert is_prime(1) is False

    # --- Larger primes ---

    def test_larger_primes(self):
        """Test with larger prime numbers."""
        assert is_prime(97) is True
        assert is_prime(101) is True
        assert is_prime(13441) is True
        assert is_prime(104729) is True  # 10000th prime

    # --- Larger non-primes ---

    def test_larger_non_primes(self):
        """Test with larger composite numbers."""
        assert is_prime(100) is False
        assert is_prime(1000) is False
        assert is_prime(10000) is False
        assert is_prime(100000) is False

    # --- Perfect squares of primes (should be non-prime) ---

    def test_perfect_square_of_prime(self):
        """Squares of primes are not prime."""
        assert is_prime(4) is False   # 2^2
        assert is_prime(9) is False   # 3^2
        assert is_prime(25) is False  # 5^2
        assert is_prime(49) is False  # 7^2

    # --- Even numbers greater than 2 ---

    def test_even_numbers_greater_than_two(self):
        """All even numbers greater than 2 are not prime."""
        for n in range(4, 100, 2):
            assert is_prime(n) is False

    # --- Return type check ---

    def test_return_type(self):
        """Ensure the function returns a boolean."""
        assert isinstance(is_prime(2), bool)
        assert isinstance(is_prime(4), bool)
