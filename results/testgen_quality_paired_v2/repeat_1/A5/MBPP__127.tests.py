# Accepted by submit_tests; explanations in testgen_report.json.

def test_multiply_basic_positive():
    from solution import multiply_int
    assert multiply_int(3, 4) == 12
    assert multiply_int(5, 6) == 30
    assert multiply_int(1, 7) == 7
    assert multiply_int(10, 10) == 100

def test_multiply_zero_cases():
    from solution import multiply_int
    assert multiply_int(0, 5) == 0
    assert multiply_int(5, 0) == 0
    assert multiply_int(-3, 0) == 0
    assert multiply_int(0, -7) == 0
    assert multiply_int(0, 0) == 0

def test_multiply_negative_y():
    from solution import multiply_int
    assert multiply_int(3, -4) == -12
    assert multiply_int(-3, -4) == 12
    assert multiply_int(5, -1) == -5
    assert multiply_int(-2, -3) == 6

def test_multiply_negative_x():
    from solution import multiply_int
    assert multiply_int(-3, 4) == -12
    assert multiply_int(-5, 2) == -10
    assert multiply_int(-1, 100) == -100
    assert multiply_int(-7, 0) == 0

def test_multiply_return_type():
    from solution import multiply_int
    result = multiply_int(3, 4)
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    result = multiply_int(-3, -4)
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    result = multiply_int(0, 0)
    assert isinstance(result, int), f'Expected int, got {type(result)}'

def test_multiply_boundary_values():
    from solution import multiply_int
    assert multiply_int(7, 1) == 7
    assert multiply_int(-7, 1) == -7
    assert multiply_int(7, -1) == -7
    assert multiply_int(-7, -1) == 7
    assert multiply_int(7, 2) == 14
    assert multiply_int(7, -2) == -14
