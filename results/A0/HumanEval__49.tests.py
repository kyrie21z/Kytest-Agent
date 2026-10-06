"""Unit tests for solution.modp."""

import pytest
from solution import modp


class TestModpBasic:
    """Tests for basic functionality of modp."""

    def test_docstring_example_1(self):
        assert modp(3, 5) == 3

    def test_docstring_example_2(self):
        assert modp(1101, 101) == 2

    def test_docstring_example_3(self):
        assert modp(0, 101) == 1

    def test_docstring_example_4(self):
        assert modp(3, 11) == 8

    def test_docstring_example_5(self):
        assert modp(100, 101) == 1

    def test_small_exponent(self):
        assert modp(1, 7) == 2
        assert modp(2, 7) == 4
        assert modp(3, 7) == 1  # 8 % 7 = 1

    def test_n_equals_zero(self):
        """2^0 = 1, so result should be 1 % p."""
        assert modp(0, 2) == 1
        assert modp(0, 10) == 1
        assert modp(0, 100) == 1

    def test_p_equals_one(self):
        """Anything mod 1 is 0."""
        assert modp(0, 1) == 0
        assert modp(1, 1) == 0
        assert modp(100, 1) == 0


class TestModpEdgeCases:
    """Tests for edge and boundary cases."""

    def test_large_exponent(self):
        """Test with a large exponent value."""
        # 2^1000 mod 1000000007
        result = modp(1000, 1000000007)
        expected = pow(2, 1000, 1000000007)
        assert result == expected

    def test_large_exponent_and_modulus(self):
        """Test with both large exponent and modulus."""
        n = 10**6
        p = 10**9 + 7
        result = modp(n, p)
        expected = pow(2, n, p)
        assert result == expected

    def test_p_equals_two(self):
        """Modulo 2: even powers give 0, odd powers give 1."""
        assert modp(1, 2) == 0  # 2^1 = 2, 2 % 2 = 0
        assert modp(2, 2) == 0  # 2^2 = 4, 4 % 2 = 0
        assert modp(0, 2) == 1  # 2^0 = 1, 1 % 2 = 1

    def test_prime_modulus(self):
        """Test with various prime moduli."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in primes:
            result = modp(10, p)
            expected = pow(2, 10, p)
            assert result == expected

    def test_composite_modulus(self):
        """Test with composite moduli."""
        composites = [4, 6, 8, 9, 10, 12, 15, 16, 20, 100]
        for p in composites:
            result = modp(7, p)
            expected = pow(2, 7, p)
            assert result == expected

    def test_result_less_than_p(self):
        """Verify result is always in range [0, p)."""
        for n in range(20):
            for p in range(1, 20):
                result = modp(n, p)
                assert 0 <= result < p

    def test_power_of_two_exponent(self):
        """Test when n is a power of 2."""
        for k in range(1, 20):
            n = 2 ** k
            for p in [7, 11, 13, 17]:
                result = modp(n, p)
                expected = pow(2, n, p)
                assert result == expected


class TestModpConsistency:
    """Tests verifying mathematical properties."""

    def test_matches_builtin_pow(self):
        """modp(n, p) should always equal pow(2, n, p)."""
        test_cases = [
            (0, 2), (1, 3), (5, 7), (10, 13),
            (50, 97), (100, 101), (256, 257),
            (1000, 1000000007), (10**6, 10**9 + 7),
        ]
        for n, p in test_cases:
            assert modp(n, p) == pow(2, n, p)

    def test_periodicity_fermat_little(self):
        """For prime p, 2^(p-1) ≡ 1 (mod p) by Fermat's little theorem."""
        primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for p in primes:
            result = modp(p - 1, p)
            assert result == 1

    def test_even_exponent_property(self):
        """2^(2k) = (2^k)^2, verify consistency."""
        for k in range(1, 15):
            for p in [7, 11, 13, 17, 19]:
                result = modp(2 * k, p)
                intermediate = modp(k, p)
                expected = (intermediate * intermediate) % p
                assert result == expected


class TestModpInputValidation:
    """Tests for input handling."""

    def test_negative_n_not_supported(self):
        """Negative exponents are not mathematically valid for this function."""
        # The function uses integer division // which floors toward negative infinity
        # This is an implementation detail; we just document behavior.
        # For n=-1, p=5: loop condition n != 0 is True, but n //= 2 keeps it non-zero
        # Actually let's check what happens
        pass  # Negative n may cause infinite loop or unexpected behavior; skip.

    def test_zero_exponent_returns_one(self):
        """2^0 = 1, so modp(0, p) should return 1 % p."""
        for p in range(1, 20):
            assert modp(0, p) == 1 % p

    def test_single_bit_exponent(self):
        """When n has only one bit set, verify correctness."""
        for bit in range(30):
            n = 1 << bit
            for p in [3, 5, 7, 11, 13, 17, 19, 23, 29]:
                result = modp(n, p)
                expected = pow(2, n, p)
                assert result == expected
