# Accepted by submit_tests; explanations in testgen_report.json.

from solution import frequency as _case0_frequency

def test_frequency_basic():
    """Count occurrences of a value appearing multiple times in a list."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is a list of integers, x is an integer present multiple times in a'
    fault_hypothesis = 'If the implementation fails to increment count correctly or skips elements, the result will be wrong.'
    oracle_reason = 'In [1, 2, 3, 2, 1], the value 2 appears at indices 1 and 3, so the count is exactly 2.'
    assert _case0_frequency([1, 2, 3, 2, 1], 2) == 2

from solution import frequency as _case1_frequency

def test_frequency_zero_occurrences():
    """Count a value that does not appear in the list; should return 0."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is a list of integers, x is an integer not present in a'
    fault_hypothesis = 'If the initial count is not zero or the loop logic is broken, a non-zero result may be returned.'
    oracle_reason = 'In [1, 2, 3], the value 5 never appears, so the count must be 0.'
    assert _case1_frequency([1, 2, 3], 5) == 0

from solution import frequency as _case2_frequency

def test_frequency_empty_list():
    """An empty list should yield a count of 0 for any search value."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is an empty list, x is any integer'
    fault_hypothesis = 'If the function does not handle empty lists gracefully, it might raise an error or return a non-zero value.'
    oracle_reason = 'With no elements to iterate over, the count variable stays at its initial value of 0.'
    assert _case2_frequency([], 1) == 0

from solution import frequency as _case3_frequency

def test_frequency_all_match():
    """When every element equals x, the count should equal the length of the list."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is a list where all elements are equal to x'
    fault_hypothesis = 'If the comparison i == x fails for some reason, the count would be less than len(a).'
    oracle_reason = 'In [5, 5, 5, 5], every element matches x=5, so the count is 4, which equals len(a).'
    assert _case3_frequency([5, 5, 5, 5], 5) == 4

from solution import frequency as _case4_frequency

def test_frequency_single_element():
    """A single-element list: if the element matches x, count is 1; otherwise 0."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is a list with exactly one element'
    fault_hypothesis = 'Off-by-one errors could cause the count to be 0 when it should be 1, or vice versa.'
    oracle_reason = 'In [42], the value 42 appears once, so frequency([42], 42) == 1. Similarly, frequency([42], 99) == 0.'
    assert _case4_frequency([42], 42) == 1
    assert _case4_frequency([42], 99) == 0

from solution import frequency as _case5_frequency

def test_frequency_negative_numbers():
    """Test with negative numbers to ensure equality comparison works correctly."""
    contract_quote = 'Write a function to count the number of occurrences of a number in a given list.'
    input_domain = 'a is a list containing negative integers, x is a negative integer'
    fault_hypothesis = 'Negative number handling could fail if sign bits or string representations are mishandled.'
    oracle_reason = 'In [-1, -2, -1, -3], the value -1 appears twice, so the count is 2.'
    assert _case5_frequency([-1, -2, -1, -3], -1) == 2
    assert _case5_frequency([-1, -2, -1, -3], -5) == 0
