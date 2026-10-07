# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_ordered():
    """Test the basic ordered case from the docstring."""
    from solution import next_smallest
    assert next_smallest([1, 2, 3, 4, 5]) == 2

def test_unordered_input():
    """Test with an unordered list of distinct integers."""
    from solution import next_smallest
    assert next_smallest([5, 1, 4, 3, 2]) == 2

def test_empty_list():
    """Test that an empty list returns None."""
    from solution import next_smallest
    assert next_smallest([]) is None

def test_all_same_elements():
    """Test that a list with all identical elements returns None."""
    from solution import next_smallest
    assert next_smallest([1, 1]) is None

def test_negative_numbers():
    """Test with negative integers to verify correct ordering."""
    from solution import next_smallest
    assert next_smallest([-5, -3, -1, -4, -2]) == -4

def test_two_distinct_elements():
    """Test with exactly two distinct elements."""
    from solution import next_smallest
    assert next_smallest([10, 5]) == 10
