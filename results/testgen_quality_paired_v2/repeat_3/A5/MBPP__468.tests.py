# Accepted by submit_tests; explanations in testgen_report.json.

from solution import max_product as _case0_max_product

def test_max_product_basic_increasing():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [1, 2, 3]. Oracle: The entire array is one contiguous non-decreasing run; product = 1*2*3 = 6.
    Fault hypothesis: Incorrect early termination or miscalculation would return < 6."""
    assert _case0_max_product([1, 2, 3]) == 6

from solution import max_product as _case1_max_product

def test_max_product_single_element():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [5]. Oracle: Only one element, so the only subsequence product is 5.
    Fault hypothesis: Off-by-one error could skip the single element entirely."""
    assert _case1_max_product([5]) == 5

from solution import max_product as _case2_max_product

def test_max_product_strictly_decreasing():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [5, 4, 3, 2, 1]. Oracle: Every adjacent pair violates non-decreasing condition; no multi-element product computed; max single element is 5.
    Fault hypothesis: Reversed comparison (< instead of >) would treat decreasing sequence as increasing."""
    assert _case2_max_product([5, 4, 3, 2, 1]) == 5

from solution import max_product as _case3_max_product

def test_max_product_equal_elements():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [2, 2, 2]. Oracle: arr[j-1] > arr[j] is never true (2 > 2 is False), so full run treated as valid; product = 2*2*2 = 8.
    Fault hypothesis: Strict inequality misuse would break at equal elements."""
    assert _case3_max_product([2, 2, 2]) == 8

from solution import max_product as _case4_max_product

def test_max_product_two_elements_increasing():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [3, 4]. Oracle: Entire array is valid non-decreasing run; product = 3*4 = 12.
    Fault hypothesis: Off-by-one in inner loop starting j at i instead of i+1."""
    assert _case4_max_product([3, 4]) == 12

from solution import max_product as _case5_max_product

def test_max_product_five_increasing():
    """Docstring quote: Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
    Input domain: [1, 2, 3, 4, 5]. Oracle: Entire array is one contiguous non-decreasing run; product = 1*2*3*4*5 = 120.
    Fault hypothesis: Loop bounds or multiplication errors would yield a smaller product."""
    assert _case5_max_product([1, 2, 3, 4, 5]) == 120
