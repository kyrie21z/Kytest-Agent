# Accepted by submit_tests; explanations in testgen_report.json.

from solution import mean_absolute_deviation as _case0_mean_absolute_deviation

def test_basic_docstring_example():
    """Verify the doctest example: [1.0, 2.0, 3.0, 4.0] yields 1.0."""
    result = _case0_mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert result == 1.0

from solution import mean_absolute_deviation as _case1_mean_absolute_deviation

def test_single_element():
    """A single-element list has zero deviation since the element equals its own mean."""
    result = _case1_mean_absolute_deviation([5.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case2_mean_absolute_deviation

def test_all_identical_elements():
    """When all elements are equal, MAD must be exactly 0."""
    result = _case2_mean_absolute_deviation([3.0, 3.0, 3.0, 3.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case3_mean_absolute_deviation

def test_negative_numbers():
    """MAD with negative numbers: [-1.0, 0.0, 1.0] should yield 2/3."""
    result = _case3_mean_absolute_deviation([-1.0, 0.0, 1.0])
    assert abs(result - 2.0 / 3.0) < 1e-12

from solution import mean_absolute_deviation as _case4_mean_absolute_deviation

def test_return_type_is_float():
    """The function must return a float, even when input contains only integers."""
    result = _case4_mean_absolute_deviation([1, 2, 3, 4])
    assert isinstance(result, float)

from solution import mean_absolute_deviation as _case5_mean_absolute_deviation

def test_mad_non_negative():
    """MAD is always >= 0 because it is an average of absolute values."""
    result = _case5_mean_absolute_deviation([-5.0, 10.0, -3.0, 7.0, 0.0])
    assert result >= 0.0
