import pytest


def test_docstring_example_1():
    """Example from docstring: 13195 = 5 * 7 * 13 * 29"""
    from solution import largest_prime_factor
    assert largest_prime_factor(13195) == 29


def test_docstring_example_2():
    """Example from docstring: 2048 = 2^11"""
    from solution import largest_prime_factor
    assert largest_prime_factor(2048) == 2


# ── Normal / typical composite inputs ──────────────────────────────

def test_largest_prime_factor_of_15():
    """15 = 3 * 5 → largest prime factor is 5"""
    from solution import largest_prime_factor
    assert largest_prime_factor(15) == 5


def test_largest_prime_factor_of_21():
    """21 = 3 * 7 → largest prime factor is 7"""
    from solution import largest_prime_factor
    assert largest_prime_factor(21) == 7


def test_largest_prime_factor_of_100():
    """100 = 2^2 * 5^2 → largest prime factor is 5"""
    from solution import largest_prime_factor
    assert largest_prime_factor(100) == 5


def test_largest_prime_factor_of_6():
    """6 = 2 * 3 → largest prime factor is 3"""
    from solution import largest_prime_factor
    assert largest_prime_factor(6) == 3


def test_largest_prime_factor_of_8():
    """8 = 2^3 → largest prime factor is 2"""
    from solution import largest_prime_factor
    assert largest_prime_factor(8) == 2


def test_largest_prime_factor_of_12():
    """12 = 2^2 * 3 → largest prime factor is 3"""
    from solution import largest_prime_factor
    assert largest_prime_factor(12) == 3


def test_largest_prime_factor_of_14():
    """14 = 2 * 7 → largest prime factor is 7"""
    from solution import largest_prime_factor
    assert largest_prime_factor(14) == 7


def test_largest_prime_factor_of_35():
    """35 = 5 * 7 → largest prime factor is 7"""
    from solution import largest_prime_factor
    assert largest_prime_factor(35) == 7


def test_largest_prime_factor_of_49():
    """49 = 7^2 → largest prime factor is 7"""
    from solution import largest_prime_factor
    assert largest_prime_factor(49) == 7


def test_largest_prime_factor_of_121():
    """121 = 11^2 → largest prime factor is 11"""
    from solution import largest_prime_factor
    assert largest_prime_factor(121) == 11


def test_largest_prime_factor_of_77():
    """77 = 7 * 11 → largest prime factor is 11"""
    from solution import largest_prime_factor
    assert largest_prime_factor(77) == 11


def test_largest_prime_factor_of_221():
    """221 = 13 * 17 → largest prime factor is 17"""
    from solution import largest_prime_factor
    assert largest_prime_factor(221) == 17


def test_largest_prime_factor_of_999():
    """999 = 3^3 * 37 → largest prime factor is 37"""
    from solution import largest_prime_factor
    assert largest_prime_factor(999) == 37


def test_largest_prime_factor_of_1000():
    """1000 = 2^3 * 5^3 → largest prime factor is 5"""
    from solution import largest_prime_factor
    assert largest_prime_factor(1000) == 5


# ── Boundary cases ─────────────────────────────────────────────────

def test_smallest_composite_4():
    """4 = 2^2 → smallest composite number; largest prime factor is 2"""
    from solution import largest_prime_factor
    assert largest_prime_factor(4) == 2


def test_two_times_small_prime():
    """2 * 3 = 6 → smallest product of two distinct primes"""
    from solution import largest_prime_factor
    assert largest_prime_factor(6) == 3


def test_large_power_of_2():
    """2^20 = 1048576 → largest prime factor is still 2"""
    from solution import largest_prime_factor
    assert largest_prime_factor(1048576) == 2


def test_product_with_large_prime():
    """2 * 97 = 194 → largest prime factor is 97"""
    from solution import largest_prime_factor
    assert largest_prime_factor(194) == 97


def test_square_of_a_prime():
    """13^2 = 169 → largest prime factor is 13"""
    from solution import largest_prime_factor
    assert largest_prime_factor(169) == 13


# ── Invalid / out-of-contract inputs ────────────────────────────────
# The docstring says "Assume n > 1 and is not a prime."
# We test what happens when these assumptions are violated.

def test_n_equals_1():
    """n = 1 violates n > 1. Function has no explicit error handling."""
    from solution import largest_prime_factor
    # With n=1: sieve size is 2, range(2,2) is empty, range(0,0,-1) is empty
    # → falls off end of function, returns None
    assert largest_prime_factor(1) is None


def test_n_equals_0():
    """n = 0 violates n > 1. Returns None per actual behavior."""
    from solution import largest_prime_factor
    assert largest_prime_factor(0) is None


def test_negative_n():
    """Negative n: [True] * -5 produces [] in Python. Loops don't execute, returns None."""
    from solution import largest_prime_factor
    assert largest_prime_factor(-5) is None


def test_n_is_prime():
    """n = 7 is prime, violating 'is not a prime' assumption.
    Index 1 stays True in the sieve, and 7 % 1 == 0, so returns 1."""
    from solution import largest_prime_factor
    assert largest_prime_factor(7) == 1


def test_n_equals_2():
    """n = 2 is prime. Same as above — returns 1."""
    from solution import largest_prime_factor
    assert largest_prime_factor(2) == 1


# ── Edge case: larger composites ────────────────────────────────────

def test_larger_composite_1001():
    """1001 = 7 * 11 * 13 → largest prime factor is 13"""
    from solution import largest_prime_factor
    assert largest_prime_factor(1001) == 13


def test_larger_composite_2310():
    """2310 = 2 * 3 * 5 * 7 * 11 → largest prime factor is 11"""
    from solution import largest_prime_factor
    assert largest_prime_factor(2310) == 11


def test_larger_composite_9999():
    """9999 = 3^2 * 11 * 101 → largest prime factor is 101"""
    from solution import largest_prime_factor
    assert largest_prime_factor(9999) == 101
