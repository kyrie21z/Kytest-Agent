"""Unit tests for solution.is_prime."""

import pytest
from solution import is_prime


class TestIsPrimeBasic:
    """Tests for basic prime and non-prime numbers."""

    def test_prime_2(self):
        assert is_prime(2) is True

    def test_prime_3(self):
        assert is_prime(3) is True

    def test_prime_5(self):
        assert is_prime(5) is True

    def test_prime_7(self):
        assert is_prime(7) is True

    def test_prime_11(self):
        assert is_prime(11) is True

    def test_prime_13(self):
        assert is_prime(13) is True

    def test_prime_17(self):
        assert is_prime(17) is True

    def test_prime_19(self):
        assert is_prime(19) is True

    def test_non_prime_4(self):
        assert is_prime(4) is False

    def test_non_prime_6(self):
        assert is_prime(6) is False

    def test_non_prime_8(self):
        assert is_prime(8) is False

    def test_non_prime_9(self):
        assert is_prime(9) is False

    def test_non_prime_10(self):
        assert is_prime(10) is False


class TestIsPrimeEdgeCases:
    """Tests for edge cases around the boundaries."""

    def test_zero(self):
        assert is_prime(0) is False

    def test_one(self):
        assert is_prime(1) is False

    def test_negative_number(self):
        assert is_prime(-5) is False

    def test_negative_one(self):
        assert is_prime(-1) is False

    def test_two_smallest_prime(self):
        assert is_prime(2) is True


class TestIsPrimeLargerNumbers:
    """Tests with larger prime and composite numbers."""

    def test_large_prime_101(self):
        assert is_prime(101) is True

    def test_large_prime_61(self):
        assert is_prime(61) is True

    def test_large_prime_13441(self):
        assert is_prime(13441) is True

    def test_composite_even_large(self):
        assert is_prime(100) is False

    def test_composite_odd_large(self):
        assert is_prime(121) is False  # 11 * 11

    def test_perfect_square_composite(self):
        assert is_prime(49) is False  # 7 * 7

    def test_perfect_square_16(self):
        assert is_prime(16) is False

    def test_perfect_square_25(self):
        assert is_prime(25) is False

    def test_perfect_square_36(self):
        assert is_prime(36) is False


class TestIsPrimeReturnTypes:
    """Tests to ensure correct return types."""

    def test_returns_bool_true(self):
        result = is_prime(7)
        assert isinstance(result, bool)
        assert result is True

    def test_returns_bool_false(self):
        result = is_prime(4)
        assert isinstance(result, bool)
        assert result is False


class TestIsPrimeDocstringExamples:
    """Tests based on the docstring examples."""

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


class TestIsPrimeComprehensive:
    """Additional comprehensive tests for thorough coverage."""

    @pytest.mark.parametrize("number, expected", [
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (7, True),
        (9, False),
        (11, True),
        (13, True),
        (15, False),
        (17, True),
        (19, True),
        (21, False),
        (23, True),
        (25, False),
        (27, False),
        (29, True),
    ])
    def test_numbers_up_to_30(self, number, expected):
        assert is_prime(number) is expected

    @pytest.mark.parametrize("number, expected", [
        (0, False),
        (-1, False),
        (-10, False),
        (-100, False),
    ])
    def test_negative_numbers(self, number, expected):
        assert is_prime(number) is expected

    @pytest.mark.parametrize("number, expected", [
        (2, True),
        (3, True),
        (5, True),
        (7, True),
        (11, True),
        (13, True),
        (17, True),
        (19, True),
        (23, True),
        (29, True),
        (31, True),
        (37, True),
        (41, True),
        (43, True),
        (47, True),
        (53, True),
        (59, True),
        (61, True),
        (67, True),
        (71, True),
        (73, True),
        (79, True),
        (83, True),
        (89, True),
        (97, True),
    ])
    def test_primes_under_100(self, number, expected):
        assert is_prime(number) is expected

    @pytest.mark.parametrize("number, expected", [
        (4, False),
        (6, False),
        (8, False),
        (9, False),
        (10, False),
        (12, False),
        (14, False),
        (15, False),
        (16, False),
        (18, False),
        (20, False),
        (21, False),
        (22, False),
        (24, False),
        (25, False),
        (26, False),
        (27, False),
        (28, False),
        (30, False),
    ])
    def test_composites_under_31(self, number, expected):
        assert is_prime(number) is expected
