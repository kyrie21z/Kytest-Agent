# Accepted by submit_tests; explanations in testgen_report.json.

import pytest as _case0_pytest

def test_next_power_of_2_one():
    """Docstring: 'Write a python function to find the smallest power of 2 greater than or equal to n.'

    Input domain: n = 1 (smallest positive integer, also a power of 2: 2^0).
    Oracle: The smallest power of 2 >= 1 is 1 itself.
    Fault hypothesis: Detects if the function fails to handle the base case n=1,
      e.g., incorrectly computing bit length instead of recognizing it as a power of 2."""
    from solution import next_power_of_2
    assert next_power_of_2(1) == 1

import pytest as _case1_pytest

def test_next_power_of_2_two():
    """Docstring: 'Write a python function to find the smallest power of 2 greater than or equal to n.'

    Input domain: n = 2 (a power of 2: 2^1).
    Oracle: Since 2 is already a power of 2, the result should be 2.
    Fault hypothesis: Detects if the early-return path for powers of 2 is broken,
      e.g., falling through to the bit-counting loop and producing a wrong result."""
    from solution import next_power_of_2
    assert next_power_of_2(2) == 2

import pytest as _case2_pytest

def test_next_power_of_2_three():
    """Docstring: 'Write a python function to find the smallest power of 2 greater than or equal to n.'

    Input domain: n = 3 (not a power of 2, between 2 and 4).
    Oracle: The smallest power of 2 >= 3 is 4 (2^2).
    Fault hypothesis: Detects off-by-one errors in the bit-counting loop,
      e.g., returning 2 instead of 4 due to undercounting shifts."""
    from solution import next_power_of_2
    assert next_power_of_2(3) == 4

import pytest as _case3_pytest

def test_next_power_of_2_zero():
    """Docstring: 'Write a python function to find the smallest power of 2 greater than or equal to n.'

    Input domain: n = 0.
    Oracle: The smallest power of 2 >= 0 is 1 (2^0 = 1). The condition `n and ...` short-circuits
      since n=0 is falsy, the loop never executes (count stays 0), and 1 << 0 = 1.
    Fault hypothesis: Detects if n=0 causes an incorrect return value,
      such as returning 0 (which is not a power of 2) or raising an error."""
    from solution import next_power_of_2
    assert next_power_of_2(0) == 1

import pytest as _case4_pytest

def test_next_power_of_2_large_power():
    """Docstring: 'Write a python function to find the smallest power of 2 greater than or equal to n.'

    Input domain: n = 1024 (a large power of 2: 2^10).
    Oracle: Since 1024 is already a power of 2, the result should be 1024.
    Fault hypothesis: Detects if the power-of-2 detection (`n & (n-1)`) fails for larger values,
      causing an incorrect fallback computation."""
    from solution import next_power_of_2
    assert next_power_of_2(1024) == 1024
