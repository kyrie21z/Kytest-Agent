# Accepted by submit_tests; explanations in testgen_report.json.

def test_max_product_single_element():
    """Test that max_product returns the single element when given a one-element list."""
    from solution import max_product
    assert max_product([7]) == 7
    assert max_product([-42]) == -42
    assert max_product([0]) == 0

def test_max_product_increasing_sequence():
    """Test max_product on a strictly increasing sequence returns the full product."""
    from solution import max_product
    assert max_product([1, 2, 3, 4, 5]) == 120
    assert max_product([2, 3, 4]) == 24
    assert max_product([1, 2]) == 2

def test_max_product_decreasing_sequence():
    """Test max_product on a decreasing sequence returns the maximum single element."""
    from solution import max_product
    assert max_product([5, 4, 3, 2, 1]) == 5
    assert max_product([3, 2, 1]) == 3
    assert max_product([10, 8, 5]) == 10

def test_max_product_plateau_and_drop():
    """Test max_product handles plateaus (equal consecutive elements) and drops correctly."""
    from solution import max_product
    assert max_product([1, 2, 2, 1, 3]) == 4
    assert max_product([3, 3, 3]) == 27
    assert max_product([2, 2]) == 4
