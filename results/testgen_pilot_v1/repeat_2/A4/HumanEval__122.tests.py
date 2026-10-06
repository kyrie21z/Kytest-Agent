# Accepted by submit_tests; explanations in testgen_report.json.

"""Test the exact example from the docstring."""
from solution import add_elements as _case0_add_elements

def test_docstring_example():
    """
    Quote: 'Input: arr = [111,21,3,4000,5,6,7,8,9], k = 4'
            'Output: 24 # sum of 21 + 3'
    Input domain: arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9], k = 4
    Oracle: From first k=4 elements [111, 21, 3, 4000]:
      - 111 has 3 digits → excluded
      - 21 has 2 digits → included
      - 3 has 1 digit → included
      - 4000 has 4 digits → excluded
      Sum = 21 + 3 = 24.
    Fault hypothesis: A bug in digit counting would produce a wrong sum.
    """
    result = _case0_add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
    assert result == 24

"""Test when all first-k elements have 1 digit each."""
from solution import add_elements as _case1_add_elements

def test_all_qualifying_single_digits():
    """
    Quote: 'return the sum of the elements with at most two digits from the first k elements'
    Input domain: arr = [1, 2, 3, 4, 5], k = 3
    Oracle: First k=3 elements are [1, 2, 3]. Each has 1 digit (≤2), so all qualify.
      Sum = 1 + 2 + 3 = 6.
    Fault hypothesis: If the slice arr[:k] were ignored or k off-by-one, sum differs.
    """
    result = _case1_add_elements([1, 2, 3, 4, 5], 3)
    assert result == 6

"""Test when no elements in first k have at most 2 digits."""
from solution import add_elements as _case2_add_elements

def test_no_qualifying_elements():
    """
    Quote: 'return the sum of the elements with at most two digits'
    Input domain: arr = [100, 200, 300], k = 3
    Oracle: First k=3 elements are [100, 200, 300]. Each has 3 digits (>2),
      so none qualify. Sum of empty set = 0.
    Fault hypothesis: Treating 3-digit numbers as qualifying would yield non-zero.
    """
    result = _case2_add_elements([100, 200, 300], 3)
    assert result == 0

"""Test negative numbers where sign is not counted as a digit."""
from solution import add_elements as _case3_add_elements

def test_negative_numbers_with_at_most_two_digits():
    """
    Quote: 'elements with at most two digits' — negative sign does not count.
    Input domain: arr = [-5, -15, 100], k = 3
    Oracle: First k=3 elements:
      - -5: str '-5', digits = len('-5') - 1 = 1 → included
      - -15: str '-15', digits = len('-15') - 1 = 2 → included
      - 100: 3 digits → excluded
      Sum = -5 + (-15) = -20.
    Fault hypothesis: Counting negative sign as a digit would exclude -15.
    """
    result = _case3_add_elements([-5, -15, 100], 3)
    assert result == -20

"""Test boundary: 99 qualifies, 100 does not."""
from solution import add_elements as _case4_add_elements

def test_boundary_two_digit_max():
    """
    Quote: 'at most two digits' — 99 qualifies, 100 does not.
    Input domain: arr = [9, 99, 100], k = 3
    Oracle: First k=3 elements:
      - 9: 1 digit → included
      - 99: 2 digits → included
      - 100: 3 digits → excluded
      Sum = 9 + 99 = 108.
    Fault hypothesis: Using < 2 instead of <= 2 would exclude 99.
    """
    result = _case4_add_elements([9, 99, 100], 3)
    assert result == 108

"""Test that the return type is int."""
from solution import add_elements as _case5_add_elements

def test_return_type_is_int():
    """
    Quote: 'return the sum' — Python's sum() on integers returns int.
    Input domain: arr = [1, 2], k = 2
    Oracle: Sum = 3, which is an int.
    Fault hypothesis: Accidentally returning float or other type would fail.
    """
    result = _case5_add_elements([1, 2], 2)
    assert isinstance(result, int)
