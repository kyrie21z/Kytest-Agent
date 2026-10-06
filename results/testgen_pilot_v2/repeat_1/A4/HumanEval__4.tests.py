# Accepted by submit_tests; explanations in testgen_report.json.

"""Test that a single-element list yields MAD of 0."""
import pytest as _case0_pytest
from solution import mean_absolute_deviation as _case0_mean_absolute_deviation

def test_single_element():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    """
    result = _case0_mean_absolute_deviation([5.0])
    assert result == _case0_pytest.approx(0.0)

"""Test that all-identical elements yield MAD of 0."""
import pytest as _case1_pytest
from solution import mean_absolute_deviation as _case1_mean_absolute_deviation

def test_all_identical():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    """
    result = _case1_mean_absolute_deviation([3.0, 3.0, 3.0, 3.0])
    assert result == _case1_pytest.approx(0.0)

"""Test MAD with negative, zero, and positive values."""
import pytest as _case2_pytest
from solution import mean_absolute_deviation as _case2_mean_absolute_deviation

def test_negative_numbers():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    """
    result = _case2_mean_absolute_deviation([-1.0, 0.0, 1.0])
    assert result == _case2_pytest.approx(2.0 / 3.0)

"""Test MAD with symmetric negative-positive list."""
import pytest as _case3_pytest
from solution import mean_absolute_deviation as _case3_mean_absolute_deviation

def test_symmetric_list():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    """
    result = _case3_mean_absolute_deviation([-2.0, -1.0, 1.0, 2.0])
    assert result == _case3_pytest.approx(1.5)

"""Test that the return type is float as annotated."""
from solution import mean_absolute_deviation as _case4_mean_absolute_deviation

def test_return_type_float():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    """
    result = _case4_mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert isinstance(result, float)

"""Test the doctest example from the docstring."""
import pytest as _case5_pytest
from solution import mean_absolute_deviation as _case5_mean_absolute_deviation

def test_docstring_example():
    """For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    """
    result = _case5_mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert result == _case5_pytest.approx(1.0)
