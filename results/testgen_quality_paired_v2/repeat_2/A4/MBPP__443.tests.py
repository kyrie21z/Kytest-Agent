# Accepted by submit_tests; explanations in testgen_report.json.

def test_single_negative():
    from solution import largest_neg
    result = largest_neg([-7])
    assert result == -7, 'Expected -7, got ' + str(result)
    assert isinstance(result, int), 'Return type should be int'

def test_return_type_check():
    from solution import largest_neg
    result = largest_neg([-5, -3, -1])
    assert isinstance(result, int), 'Return value should be int, got ' + str(type(result))
