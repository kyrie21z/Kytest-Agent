# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_X as _case0_count_X

def test_count_single_occurrence():
    """Test that count_X correctly counts a single occurrence of an element in a tuple.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: A non-empty tuple with exactly one instance of the target element.
    Oracle: The returned count must equal 1 since the element appears exactly once.
    Fault hypothesis: Counter initialized incorrectly or incremented wrong number of times."""
    assert _case0_count_X(('a', 'b', 'c'), 'b') == 1

from solution import count_X as _case1_count_X

def test_count_multiple_occurrences():
    """Test that count_X correctly counts multiple occurrences of an element.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: A tuple where the target element appears 3 times among other elements.
    Oracle: Since 'a' appears 3 times in ('a', 'b', 'a', 'c', 'a'), the result must be 3.
    Fault hypothesis: Detects early termination or incomplete iteration over the tuple."""
    assert _case1_count_X(('a', 'b', 'a', 'c', 'a'), 'a') == 3

from solution import count_X as _case2_count_X

def test_count_no_occurrence():
    """Test that count_X returns 0 when the element is not present in the tuple.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: A tuple where the target element does not appear at all.
    Oracle: Since 'z' is not in ('a', 'b', 'c'), the count must be 0.
    Fault hypothesis: Detects returning a non-zero default or miscounting absent elements."""
    assert _case2_count_X(('a', 'b', 'c'), 'z') == 0

from solution import count_X as _case3_count_X

def test_count_empty_tuple():
    """Test that count_X returns 0 for an empty tuple.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: An empty tuple () with any element as the search target.
    Oracle: Iterating over an empty tuple produces no matches, so count must be 0.
    Fault hypothesis: Detects handling of edge case where tuple has zero length."""
    assert _case3_count_X((), 5) == 0

from solution import count_X as _case4_count_X

def test_count_all_same_elements():
    """Test that count_X counts all elements when every element matches the target.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: A tuple where every element equals the search target.
    Oracle: In (5, 5, 5, 5, 5), the element 5 appears 5 times, so count must be 5.
    Fault hypothesis: Detects undercounting when all elements are identical."""
    assert _case4_count_X((5, 5, 5, 5, 5), 5) == 5

from solution import count_X as _case5_count_X

def test_count_integer_types():
    """Test that count_X works correctly with integer elements.
    
    Contract quote: "takes in a tuple and an element and counts the occcurences of the element in the tuple."
    Input domain: A tuple of integers with the target appearing twice.
    Oracle: In (1, 2, 3, 2, 4), the element 2 appears 2 times, so count must be 2.
    Fault hypothesis: Detects type-specific comparison failures with integers."""
    assert _case5_count_X((1, 2, 3, 2, 4), 2) == 2
