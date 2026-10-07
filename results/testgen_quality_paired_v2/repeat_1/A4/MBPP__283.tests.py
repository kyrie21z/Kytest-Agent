# Accepted by submit_tests; explanations in testgen_report.json.

def test_single_digit_valid():
    from solution import validate
    assert validate(5) is True

def test_repeated_digit_exceeds_limit():
    from solution import validate
    assert validate(11) is False

def test_contains_zero_digit():
    from solution import validate
    assert validate(10) is False

def test_zero_input():
    from solution import validate
    assert validate(0) is True

def test_three_of_digit_3_boundary():
    from solution import validate
    assert validate(333) is True
    assert validate(3333) is False

def test_mixed_digits_all_valid():
    from solution import validate
    assert validate(22345) is True
    assert validate(2234511) is False
