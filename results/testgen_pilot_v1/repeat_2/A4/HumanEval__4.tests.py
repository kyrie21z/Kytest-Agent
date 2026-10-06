# Accepted by submit_tests; explanations in testgen_report.json.

import math as _case0_math
from solution import mean_absolute_deviation as _case0_mean_absolute_deviation

def test_mad_basic_example():
    """Test the doctest example: [1,2,3,4] should give MAD = 1.0."""
    result = _case0_mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert abs(result - 1.0) < 1e-09

from solution import mean_absolute_deviation as _case1_mean_absolute_deviation

def test_mad_single_element():
    """For a single-element list, MAD must be 0 since the only element equals the mean."""
    result = _case1_mean_absolute_deviation([5.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case2_mean_absolute_deviation

def test_mad_symmetric_list():
    """For a symmetric list around its mean, MAD can be computed directly.
    [-2, -1, 0, 1, 2]: mean=0, sum of abs devs = 2+1+0+1+2=6, MAD=6/5=1.2"""
    result = _case2_mean_absolute_deviation([-2.0, -1.0, 0.0, 1.0, 2.0])
    assert abs(result - 1.2) < 1e-09

from solution import mean_absolute_deviation as _case3_mean_absolute_deviation

def test_mad_all_same_elements():
    """When all elements are identical, MAD must be 0."""
    result = _case3_mean_absolute_deviation([7.0, 7.0, 7.0, 7.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case4_mean_absolute_deviation

def test_mad_two_elements():
    """For two elements, MAD = half the absolute difference between them.
    [0, 10]: mean=5, |0-5|+|10-5|=5+5=10, MAD=10/2=5"""
    result = _case4_mean_absolute_deviation([0.0, 10.0])
    assert abs(result - 5.0) < 1e-09
