# Accepted by submit_tests; explanations in testgen_report.json.

"""Test the exact example from the docstring."""
from solution import add_elements as _case0_add_elements

def test_docstring_example():
    """Contract quote: 'Input: arr = [111,21,3,4000,5,6,7,8,9], k = 4, Output: 24 # sum of 21 + 3'
    Input domain: arr is a list of ints with len >= 1, k=4 satisfies 1<=k<=len(arr).
    Oracle: Among the first 4 elements [111, 21, 3, 4000], only 21 (2 digits) and 3 (1 digit)
    have at most 2 digits. Sum = 21 + 3 = 24. 111 has 3 digits, 4000 has 4 digits — both excluded.
    Fault hypothesis: Detects if the function incorrectly includes multi-digit (>2) numbers
    or miscalculates the sum."""
    result = _case0_add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
    assert result == 24

"""Test when no elements in the first k have at most 2 digits."""
from solution import add_elements as _case1_add_elements

def test_no_elements_qualify():
    """Contract quote: 'return the sum of the elements with at most two digits from the first k elements'
    Input domain: arr=[100, 200, 300], k=3; all elements have 3 digits.
    Oracle: No element in arr[:3] has <= 2 digits. Sum of empty set = 0.
    Fault hypothesis: Detects if the function returns a non-zero value when no elements qualify."""
    result = _case1_add_elements([100, 200, 300], 3)
    assert result == 0

"""Test digit counting for negative numbers."""
from solution import add_elements as _case2_add_elements

def test_negative_numbers():
    """Contract quote: 'elements with at most two digits' — negatives count digits excluding sign.
    Input domain: arr=[-5, -12, 100], k=3.
    Oracle: -5 has 1 digit, -12 has 2 digits, 100 has 3 digits. Qualifying: -5 + (-12) = -17.
    Fault hypothesis: Detects incorrect digit counting for negative numbers (e.g., treating '-' as a digit)."""
    result = _case2_add_elements([-5, -12, 100], 3)
    assert result == -17

"""Test boundary between 2-digit and 3-digit numbers."""
from solution import add_elements as _case3_add_elements

def test_boundary_2vs3_digits():
    """Contract quote: 'at most two digits' — boundary between qualifying and non-qualifying.
    Input domain: arr=[99, 100, -99, -100], k=4.
    Oracle: 99 has 2 digits (qualifies), 100 has 3 digits (excluded), -99 has 2 digits (qualifies),
    -100 has 4 chars including '-' → 3 digits (excluded). Sum = 99 + (-99) = 0.
    Fault hypothesis: Detects off-by-one errors at the 2/3 digit boundary."""
    result = _case3_add_elements([99, 100, -99, -100], 4)
    assert result == 0

"""Test that only the first k elements are considered."""
from solution import add_elements as _case4_add_elements

def test_k_scope_limitation():
    """Contract quote: 'from the first k elements of arr' — elements beyond index k-1 must be ignored.
    Input domain: arr=[1, 2, 3, 4, 500], k=3.
    Oracle: First 3 elements are [1, 2, 3]; all have <= 2 digits. 500 is beyond k, ignored.
    Sum = 1 + 2 + 3 = 6.
    Fault hypothesis: Detects if the function considers elements beyond index k-1."""
    result = _case4_add_elements([1, 2, 3, 4, 500], 3)
    assert result == 6

"""Test when all elements in the first k have at most 2 digits."""
from solution import add_elements as _case5_add_elements

def test_all_qualify_single_digit():
    """Contract quote: 'return the sum of the elements with at most two digits from the first k elements'
    Input domain: arr=[1, 2, 3], k=3; all elements are single-digit.
    Oracle: Every element in arr[:3] has <= 2 digits. Sum = 1 + 2 + 3 = 6.
    Fault hypothesis: Detects if the function fails when every element qualifies (e.g., returns 0)."""
    result = _case5_add_elements([1, 2, 3], 3)
    assert result == 6
