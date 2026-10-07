# Accepted by submit_tests; explanations in testgen_report.json.

def test_multiply_positive():
    from solution import multiply_int
    assert multiply_int(3, 4) == 12
    assert multiply_int(7, 8) == 56
    assert multiply_int(1, 1) == 1
    assert multiply_int(10, 10) == 100

def test_multiply_zero_y():
    from solution import multiply_int
    assert multiply_int(5, 0) == 0
    assert multiply_int(-3, 0) == 0
    assert multiply_int(0, 0) == 0

def test_multiply_negative_y():
    from solution import multiply_int
    assert multiply_int(3, -4) == -12
    assert multiply_int(-3, -4) == 12
    assert multiply_int(5, -1) == -5
    assert multiply_int(-5, -1) == 5

def test_multiply_negative_x():
    from solution import multiply_int
    assert multiply_int(-3, 4) == -12
    assert multiply_int(-7, 2) == -14
    assert multiply_int(-1, 5) == -5

def test_multiply_identity():
    from solution import multiply_int
    assert multiply_int(42, 1) == 42
    assert multiply_int(-42, 1) == -42
    assert multiply_int(0, 1) == 0

def test_multiply_y_equals_one_nonzero():
    from solution import multiply_int
    assert multiply_int(99, 1) == 99
    assert multiply_int(-99, 1) == -99
    assert multiply_int(1, 1) == 1
