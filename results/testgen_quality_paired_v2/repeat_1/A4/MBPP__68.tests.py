# Accepted by submit_tests; explanations in testgen_report.json.

from solution import is_Monotonic as _case0_is_Monotonic

def test_empty_list():
    """Verify that an empty list is considered monotonic.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: For an empty list, len(A) == 0, so range(len(A)-1) == range(-1) which is empty.
    all() over an empty iterable returns True in Python. Thus both branches of the OR evaluate to True,
    and the result is True. This is mathematically sound: vacuous truth — there is no pair of adjacent
    elements that violates either ordering.
    
    Fault hypothesis: If the implementation incorrectly raises an IndexError on empty input, or returns
    False for empty lists, this test will catch it by asserting True.
    """
    assert _case0_is_Monotonic([]) is True

from solution import is_Monotonic as _case1_is_Monotonic

def test_single_element():
    """Verify that a single-element list is monotonic.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: For a list with one element, len(A) == 1, so range(len(A)-1) == range(0) which
    is empty. all() over an empty iterable returns True. A single element trivially satisfies both
    non-decreasing and non-increasing properties.
    
    Fault hypothesis: If the function fails to handle single-element lists (e.g., off-by-one error
    accessing A[i+1] when i == 0 and len == 1), this would raise an IndexError.
    """
    assert _case1_is_Monotonic([42]) is True

from solution import is_Monotonic as _case2_is_Monotonic

def test_strictly_increasing():
    """Verify that a strictly increasing list is detected as monotonic.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: The sequence [1, 2, 3, 4, 5] satisfies A[i] <= A[i+1] for all valid i:
      1<=2, 2<=3, 3<=4, 4<=5 — all True. Therefore the first branch of the OR returns True.
    The second branch (non-increasing) returns False, but the overall result is True.
    
    Fault hypothesis: If the comparison operator is wrong (e.g., using < instead of <=), this still
    passes since strict inequality holds. But if the logic were inverted (checking >= only), it would
    fail. More importantly, if the function mistakenly returned False for any increasing sequence,
    this catches it.
    """
    assert _case2_is_Monotonic([1, 2, 3, 4, 5]) is True

from solution import is_Monotonic as _case3_is_Monotonic

def test_strictly_decreasing():
    """Verify that a strictly decreasing list is detected as monotonic.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: The sequence [5, 4, 3, 2, 1] satisfies A[i] >= A[i+1] for all valid i:
      5>=4, 4>=3, 3>=2, 2>=1 — all True. Therefore the second branch of the OR returns True.
    The first branch (non-decreasing) returns False, but the overall result is True.
    
    Fault hypothesis: If the function only checks non-decreasing order and ignores non-increasing,
    this test would return False incorrectly.
    """
    assert _case3_is_Monotonic([5, 4, 3, 2, 1]) is True

from solution import is_Monotonic as _case4_is_Monotonic

def test_non_monotonic():
    """Verify that a non-monotonic list is correctly identified.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: The sequence [1, 3, 2] has pairs (1,3), (3,2). For non-decreasing: 1<=3 is True
    but 3<=2 is False, so first all() returns False. For non-increasing: 1>=3 is False, so second
    all() returns False immediately. Overall result is False.
    
    Fault hypothesis: If the function incorrectly returns True for this case (e.g., due to short-
    circuit issues or wrong logic), this assertion will fail. Also catches bugs where the function
    only checks one direction.
    """
    assert _case4_is_Monotonic([1, 3, 2]) is False

from solution import is_Monotonic as _case5_is_Monotonic

def test_constant_elements():
    """Verify that a constant list (all equal elements) is monotonic.
    
    Contract quote: 'Write a python function to check whether the given array is monotonic or not.'
    
    Oracle reasoning: The sequence [3, 3, 3, 3] satisfies both A[i] <= A[i+1] AND A[i] >= A[i+1]
    for every adjacent pair since 3==3. Both all() calls return True, and True or True is True.
    A constant sequence is both non-decreasing and non-increasing.
    
    Fault hypothesis: If the function uses strict comparisons (< or >) instead of non-strict (<= or >=),
    this would return False incorrectly, since no element is strictly less than or greater than its neighbor.
    """
    assert _case5_is_Monotonic([7, 7, 7, 7]) is True
