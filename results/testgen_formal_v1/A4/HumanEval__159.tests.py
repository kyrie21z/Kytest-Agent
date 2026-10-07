# Accepted by submit_tests; explanations in testgen_report.json.

def test_return_type_and_structure():
    from solution import eat
    r1 = eat(5, 6, 10)
    r2 = eat(2, 11, 5)
    assert isinstance(r1, list)
    assert len(r1) == 2
    assert isinstance(r1[0], int)
    assert isinstance(r1[1], int)
    assert isinstance(r2, list)
    assert len(r2) == 2
    assert isinstance(r2[0], int)
    assert isinstance(r2[1], int)

def test_basic_need_leq_remaining():
    from solution import eat
    result = eat(5, 6, 10)
    assert result == [11, 4]

def test_need_exceeds_remaining():
    from solution import eat
    result = eat(2, 11, 5)
    assert result == [7, 0]

def test_need_equals_remaining():
    from solution import eat
    result = eat(1, 10, 10)
    assert result == [11, 0]

def test_zero_need():
    from solution import eat
    result = eat(5, 0, 10)
    assert result == [5, 10]

def test_all_zeros():
    from solution import eat
    result = eat(0, 0, 0)
    assert result == [0, 0]
