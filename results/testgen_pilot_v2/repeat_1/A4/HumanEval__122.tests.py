# Accepted by submit_tests; explanations in testgen_report.json.

from solution import add_elements as _case0_add_elements

def test_docstring_example():
    """
    Contract quote: 'Input: arr = [111,21,3,4000,5,6,7,8,9], k = 4
        Output: 24 # sum of 21 + 3'
    Input domain: arr = [111,21,3,4000,5,6,7,8,9], k = 4
    Oracle: First k=4 elements are [111, 21, 3, 4000]. Among these:
      - 111 has 3 digits -> excluded
      - 21 has 2 digits -> included
      - 3 has 1 digit -> included
      - 4000 has 4 digits -> excluded
      Sum = 21 + 3 = 24.
    Fault hypothesis: A buggy implementation might include all first-k elements regardless of digit count,
    or miscount digits for multi-digit numbers.
    """
    result = _case0_add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
    assert result == 24

from solution import add_elements as _case1_add_elements

def test_all_qualify():
    """
    Contract quote: 'return
    the sum of the elements with at most two digits from the first k elements of arr.'
    Input domain: arr = [1, 2, 3], k = 3
    Oracle: All three elements have 1 digit each (<=2), so all are included. Sum = 1 + 2 + 3 = 6.
    Fault hypothesis: If the filter condition is inverted or wrong, some qualifying elements could be excluded.
    """
    result = _case1_add_elements([1, 2, 3], 3)
    assert result == 6

from solution import add_elements as _case2_add_elements

def test_none_qualify():
    """
    Contract quote: 'return
    the sum of the elements with at most two digits from the first k elements of arr.'
    Input domain: arr = [100, 200, 300], k = 3
    Oracle: All elements have 3 digits (>2), so none qualify. Sum = 0.
    Fault hypothesis: A bug that always includes elements would yield 600.
    """
    result = _case2_add_elements([100, 200, 300], 3)
    assert result == 0

from solution import add_elements as _case3_add_elements

def test_negative_numbers():
    """
    Contract quote: 'return
    the sum of the elements with at most two digits from the first k elements of arr.'
    Input domain: arr = [-5, -99, -100, 50], k = 4
    Oracle: Using digits() which excludes the minus sign:
      - -5: str('-5') has length 2, minus sign stripped => 1 digit -> included
      - -99: str('-99') has length 3, minus sign stripped => 2 digits -> included
      - -100: str('-100') has length 4, minus sign stripped => 3 digits -> excluded
      - 50: 2 digits -> included
      Sum = -5 + (-99) + 50 = -54.
    Fault hypothesis: Miscounting digits for negative numbers (e.g., counting '-' as a digit) would incorrectly
    include -100 or exclude valid negatives.
    """
    result = _case3_add_elements([-5, -99, -100, 50], 4)
    assert result == -54

from solution import add_elements as _case4_add_elements

def test_boundary_values():
    """
    Contract quote: 'return
    the sum of the elements with at most two digits from the first k elements of arr.'
    Input domain: arr = [99, 100, -99, -100, 0], k = 5
    Oracle: 
      - 99: 2 digits -> included
      - 100: 3 digits -> excluded
      - -99: 2 digits (excluding '-') -> included
      - -100: 3 digits (excluding '-') -> excluded
      - 0: 1 digit -> included
      Sum = 99 + (-99) + 0 = 0.
    Fault hypothesis: Off-by-one in digit threshold (using < 2 instead of <= 2) would exclude 99 and -99,
    yielding only 0.
    """
    result = _case4_add_elements([99, 100, -99, -100, 0], 5)
    assert result == 0

from solution import add_elements as _case5_add_elements

def test_k_equals_len():
    """
    Contract quote: 'return
    the sum of the elements with at most two digits from the first k elements of arr.'
    Input domain: arr = [5, 10, 15, 20, 999], k = 5
    Oracle: All 5 elements are considered:
      - 5: 1 digit -> included
      - 10: 2 digits -> included
      - 15: 2 digits -> included
      - 20: 2 digits -> included
      - 999: 3 digits -> excluded
      Sum = 5 + 10 + 15 + 20 = 50.
    Fault hypothesis: If k slicing is wrong (e.g., arr[:k-1]), the last qualifying element before 999 might be missed.
    """
    result = _case5_add_elements([5, 10, 15, 20, 999], 5)
    assert result == 50
