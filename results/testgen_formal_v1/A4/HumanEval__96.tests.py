# Accepted by submit_tests; explanations in testgen_report.json.

def test_count_up_to_example_5():
    from solution import count_up_to
    result = count_up_to(5)
    assert result == [2, 3]
    assert isinstance(result, list)

def test_count_up_to_example_11():
    from solution import count_up_to
    result = count_up_to(11)
    assert result == [2, 3, 5, 7]
    assert len(result) == 4

def test_count_up_to_zero():
    from solution import count_up_to
    result = count_up_to(0)
    assert result == []
    assert isinstance(result, list)

def test_count_up_to_one():
    from solution import count_up_to
    result = count_up_to(1)
    assert result == []
    assert isinstance(result, list)

def test_count_up_to_twenty():
    from solution import count_up_to
    result = count_up_to(20)
    assert result == [2, 3, 5, 7, 11, 13, 17, 19]
    assert len(result) == 8
    for p in result:
        assert p >= 2
        for d in range(2, int(p ** 0.5) + 1):
            assert p % d != 0
    composites_below_20 = {4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20}
    for c in composites_below_20:
        assert c not in result

def test_count_up_to_boundary_and_type():
    from solution import count_up_to
    result = count_up_to(2)
    assert result == []
    assert isinstance(result, list)
    result = count_up_to(3)
    assert result == [2]
    assert isinstance(result, list)
    result = count_up_to(4)
    assert result == [2, 3]
    for n in [0, 1, 2, 10, 100]:
        r = count_up_to(n)
        assert isinstance(r, list), f'Expected list for n={n}, got {type(r)}'
