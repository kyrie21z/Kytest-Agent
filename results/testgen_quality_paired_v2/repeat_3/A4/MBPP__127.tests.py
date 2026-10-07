# Accepted by submit_tests; explanations in testgen_report.json.

from solution import multiply_int as _case0_multiply_int

def test_basic_positive():
    """Verify basic positive integer multiplication."""
    assert _case0_multiply_int(3, 4) == 12
    assert _case0_multiply_int(7, 2) == 14
    assert _case0_multiply_int(10, 10) == 100

from solution import multiply_int as _case1_multiply_int

def test_zero_handling():
    """Verify that multiplying by zero yields zero regardless of the other operand."""
    assert _case1_multiply_int(5, 0) == 0
    assert _case1_multiply_int(0, 5) == 0
    assert _case1_multiply_int(0, 0) == 0
    assert _case1_multiply_int(-3, 0) == 0

from solution import multiply_int as _case2_multiply_int

def test_negative_y():
    """Verify correct behavior when y is negative."""
    assert _case2_multiply_int(3, -4) == -12
    assert _case2_multiply_int(7, -1) == -7
    assert _case2_multiply_int(1, -5) == -5

from solution import multiply_int as _case3_multiply_int

def test_both_negative():
    """Verify that two negatives yield a positive product."""
    assert _case3_multiply_int(-3, -4) == 12
    assert _case3_multiply_int(-2, -5) == 10
    assert _case3_multiply_int(-1, -1) == 1

from solution import multiply_int as _case4_multiply_int

def test_return_type():
    """Verify the return value is always an int."""
    for x, y in [(3, 4), (0, 0), (-5, 3), (5, -2), (-3, -4)]:
        result = _case4_multiply_int(x, y)
        assert isinstance(result, int), f'Expected int but got {type(result).__name__} for ({x}, {y})'

from solution import multiply_int as _case5_multiply_int

def test_large_values():
    """Verify correctness with moderately larger integer values."""
    assert _case5_multiply_int(10, 10) == 100
    assert _case5_multiply_int(20, -3) == -60
    assert _case5_multiply_int(-7, 5) == -35
