# Accepted by submit_tests; explanations in testgen_report.json.

from solution import factorize as _case0_factorize

def test_factorize_basic_examples():
    """Test the three examples from the docstring."""
    assert _case0_factorize(8) == [2, 2, 2]
    assert _case0_factorize(25) == [5, 5]
    assert _case0_factorize(70) == [2, 5, 7]

from solution import factorize as _case1_factorize

def test_factorize_prime_number():
    """A prime number should return a single-element list containing itself."""
    assert _case1_factorize(7) == [7]
    assert _case1_factorize(13) == [13]
    assert _case1_factorize(97) == [97]

from solution import factorize as _case2_factorize

def test_factorize_product_property():
    """The product of all returned factors must equal the original input."""
    import math
    for n in range(2, 101):
        factors = _case2_factorize(n)
        product = 1
        for f in factors:
            product *= f
        assert product == n, f'Product mismatch for {n}: factors={factors}, product={product}'
        assert factors == sorted(factors), f'Factors not sorted for {n}: {factors}'
        for f in factors:
            assert f >= 2
            for d in range(2, int(math.isqrt(f)) + 1):
                assert f % d != 0, f'{f} is not prime but appears in factorization of {n}'

from solution import factorize as _case3_factorize

def test_factorize_power_of_two():
    """Powers of two should yield only 2s in the result."""
    assert _case3_factorize(2) == [2]
    assert _case3_factorize(4) == [2, 2]
    assert _case3_factorize(16) == [2, 2, 2, 2]
    assert _case3_factorize(1024) == [2] * 10

from solution import factorize as _case4_factorize

def test_factorize_square_number():
    """Perfect squares should have each prime factor appearing an even number of times."""
    assert _case4_factorize(4) == [2, 2]
    assert _case4_factorize(9) == [3, 3]
    assert _case4_factorize(36) == [2, 2, 3, 3]
    assert _case4_factorize(49) == [7, 7]
    assert _case4_factorize(121) == [11, 11]

from solution import factorize as _case5_factorize

def test_factorize_return_type():
    """Return value must always be a list of integers."""
    result = _case5_factorize(6)
    assert isinstance(result, list)
    assert all((isinstance(x, int) for x in result))
    result1 = _case5_factorize(1)
    assert isinstance(result1, list)
