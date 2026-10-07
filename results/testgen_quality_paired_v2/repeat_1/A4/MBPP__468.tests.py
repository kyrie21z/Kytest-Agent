# Accepted by submit_tests; explanations in testgen_report.json.

"""Test single element array."""
from solution import max_product as _case0_max_product

def test_single_element():
    """Contract: return the product of an increasing subsequence.
    Quote: 'Write a function to find the maximum product formed by multiplying
            numbers of an increasing subsequence of that array.'
    Input domain: arr = [7] — a single-element list.
    Oracle: With only one element, the only non-empty contiguous non-decreasing
            subsequence is [7], whose product is 7. Expected result: 7.
    Fault hypothesis: If the function mishandles n==1 (e.g., returns 0 or raises),
            this catches it."""
    assert _case0_max_product([7]) == 7

"""Test strictly increasing three-element array."""
from solution import max_product as _case1_max_product

def test_strictly_increasing_three():
    """Quote: '...maximum product formed by multiplying numbers of an increasing
              subsequence...'
    Input domain: arr = [2, 3, 4] — three distinct elements in ascending order.
    Oracle: The entire array is one contiguous non-decreasing run. Product = 2*3*4 = 24.
            Any shorter sub-segment has smaller product (all factors ≥ 2).
            Expected result: 24.
    Fault hypothesis: If the function fails to multiply across the full run,
            e.g., returns only 4 or 6 instead of 24."""
    assert _case1_max_product([2, 3, 4]) == 24

"""Test strictly decreasing array."""
from solution import max_product as _case2_max_product

def test_strictly_decreasing():
    """Quote: '...maximum product formed by multiplying numbers of an increasing
              subsequence...'
    Input domain: arr = [5, 3, 1] — strictly decreasing sequence.
    Oracle: No pair satisfies arr[j-1] <= arr[j], so no two-element contiguous
            non-decreasing run exists. The best is a single element, max = 5.
            Expected result: 5.
    Fault hypothesis: If the function incorrectly combines elements from
            non-contiguous positions or misinterprets decreasing sequences."""
    assert _case2_max_product([5, 3, 1]) == 5

"""Test equal adjacent elements."""
from solution import max_product as _case3_max_product

def test_equal_adjacent_elements():
    """Quote: '...increasing subsequence...'
    Input domain: arr = [3, 3, 3] — all equal elements.
    Oracle: Since arr[j-1] > arr[j] is False for equal neighbors, the entire
            array forms a valid contiguous non-decreasing run. Product = 3*3*3 = 27.
            Expected result: 27.
    Fault hypothesis: If the function treats equality as a break condition
            (using >= instead of >), it would return 3 instead of 27."""
    assert _case3_max_product([3, 3, 3]) == 27

"""Test two segments where the second is longer and better."""
from solution import max_product as _case4_max_product

def test_two_segments_best_is_longer():
    """Quote: '...maximum product formed by multiplying numbers of an increasing
              subsequence...'
    Input domain: arr = [1, 2, 3, 1, 2, 3, 4, 5] — two non-decreasing runs.
    Oracle: First run [1,2,3] → product 6. Second run [1,2,3,4,5] → product 120.
            Max is 120.
            Expected result: 120.
    Fault hypothesis: If the function picks the first run's product (6) instead
            of the globally best run."""
    assert _case4_max_product([1, 2, 3, 1, 2, 3, 4, 5]) == 120

"""Test zero between positives."""
from solution import max_product as _case5_max_product

def test_zero_in_middle():
    """Quote: '...maximum product formed by multiplying numbers of an increasing
              subsequence...'
    Input domain: arr = [2, 0, 3] — zero between positives.
    Oracle: Run [2] → product 2. Run [0, 3] → product 0. Single elements: 2, 0, 3.
            Max among all mpis entries: max(2, 0, 3) = 3.
            Expected result: 3.
    Fault hypothesis: If the function returns 0 (product of [0,3]) instead of 3."""
    assert _case5_max_product([2, 0, 3]) == 3

"""Test negative numbers with zero and positive."""
from solution import max_product as _case6_max_product

def test_negative_numbers_fixed():
    """Quote: '...maximum product formed by multiplying numbers of an increasing
              subsequence...'
    Input domain: arr = [-5, -3, -1, 0, 2] — negatives followed by zero and positive.
    Oracle: Tracing the algorithm:
      i=0: current_prod=-5; j=1: -5<=-3, prod=(-5)*(-3)=15, mpis[1]=max(-3,15)=15;
           j=2: -3<=-1, prod=15*(-1)=-15, mpis[2]=max(-1,-15)=-1;
           j=3: -1<=0, prod=-15*0=0, mpis[3]=max(0,0)=0;
           j=4: 0<=2, prod=0*2=0, mpis[4]=max(2,0)=2.
      i=1: current_prod=-3; j=2: -3<=-1, prod=(-3)*(-1)=3, mpis[2]=max(-1,3)=3;
           j=3: -1<=0, prod=3*0=0, mpis[3]=max(0,0)=0;
           j=4: 0<=2, prod=0*2=0, mpis[4]=max(2,0)=2.
      i=2: current_prod=-1; j=3: -1<=0, prod=-1*0=0, mpis[3]=max(0,0)=0;
           j=4: 0<=2, prod=0*2=0, mpis[4]=max(2,0)=2.
      i=3: current_prod=0; j=4: 0<=2, prod=0*2=0, mpis[4]=max(2,0)=2.
      i=4: current_prod=2.
      Final mpis=[-5,15,-1,0,2], max=15.
            Expected result: 15.
    Fault hypothesis: If the function fails to capture the positive product
            from two negatives (e.g., returns 2 or 0)."""
    assert _case6_max_product([-5, -3, -1, 0, 2]) == 15
