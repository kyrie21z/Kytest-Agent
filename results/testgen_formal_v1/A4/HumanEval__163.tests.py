# Accepted by submit_tests; explanations in testgen_report.json.

"""Test basic case from docstring: generate_integers(2, 8) => [2, 4, 6, 8]."""
from solution import generate_integers as _case0_generate_integers

def test_even_digits_basic():
    result = _case0_generate_integers(2, 8)
    assert result == [2, 4, 6, 8]

"""Test swapped arguments from docstring: generate_integers(8, 2) => [2, 4, 6, 8]."""
from solution import generate_integers as _case1_generate_integers

def test_reversed_arguments():
    result = _case1_generate_integers(8, 2)
    assert result == [2, 4, 6, 8]

"""Test case from docstring: generate_integers(10, 14) => []."""
from solution import generate_integers as _case2_generate_integers

def test_no_even_digits_in_range():
    result = _case2_generate_integers(10, 14)
    assert result == []

"""Test when a == b and the value is even."""
from solution import generate_integers as _case3_generate_integers

def test_equal_even_bounds():
    result = _case3_generate_integers(4, 4)
    assert result == [4]

"""Test that values above 9 do not affect the result."""
from solution import generate_integers as _case4_generate_integers

def test_upper_bound_capped_at_9():
    result = _case4_generate_integers(2, 100)
    assert result == [2, 4, 6, 8]

"""Verify the return type is always a list and check full single-digit range."""
from solution import generate_integers as _case5_generate_integers

def test_return_type_and_full_range():
    result = _case5_generate_integers(1, 9)
    assert isinstance(result, list)
    assert result == [2, 4, 6, 8]
