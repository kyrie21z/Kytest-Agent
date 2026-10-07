# Accepted by submit_tests; explanations in testgen_report.json.

def test_collatz_n5():
    """Test that get_odd_collatz(5) returns [1, 5] as documented."""
    from solution import get_odd_collatz
    result = get_odd_collatz(5)
    assert result == [1, 5]

def test_collatz_n1():
    """Test that get_odd_collatz(1) returns [1]."""
    from solution import get_odd_collatz
    result = get_odd_collatz(1)
    assert result == [1]

def test_collatz_n3():
    """Test that get_odd_collatz(3) returns [1, 3, 5]."""
    from solution import get_odd_collatz
    result = get_odd_collatz(3)
    assert result == [1, 3, 5]

def test_collatz_n7():
    """Test that get_odd_collatz(7) returns [1, 5, 7, 11, 13, 17]."""
    from solution import get_odd_collatz
    result = get_odd_collatz(7)
    assert result == [1, 5, 7, 11, 13, 17]

def test_collatz_return_type():
    """Test that get_odd_collatz returns a list (not tuple or other type)."""
    from solution import get_odd_collatz
    result = get_odd_collatz(5)
    assert isinstance(result, list)

def test_collatz_n2():
    """Test that get_odd_collatz(2) returns [1] since 2 is even."""
    from solution import get_odd_collatz
    result = get_odd_collatz(2)
    assert result == [1]
