# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_increasing():
    from solution import rearrange_bigger
    assert rearrange_bigger(12) == 21

def test_no_bigger_possible_descending():
    from solution import rearrange_bigger
    assert rearrange_bigger(321) is False

def test_single_digit():
    from solution import rearrange_bigger
    assert rearrange_bigger(5) is False

def test_repeated_digits():
    from solution import rearrange_bigger
    assert rearrange_bigger(1221) == 2112

def test_return_type_int_on_success():
    from solution import rearrange_bigger
    result = rearrange_bigger(123)
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    assert result == 132

def test_all_same_digits():
    from solution import rearrange_bigger
    assert rearrange_bigger(111) is False
