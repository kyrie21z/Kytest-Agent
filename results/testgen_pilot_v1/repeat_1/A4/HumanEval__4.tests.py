# Accepted by submit_tests; explanations in testgen_report.json.

from solution import mean_absolute_deviation as _case0_mean_absolute_deviation

def test_docstring_example():
    """Verify the doctest example: [1.0, 2.0, 3.0, 4.0] -> 1.0.

    Contract quote: ">>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0"
    Input domain: A list of four positive floats forming an arithmetic progression.
    Expected result: mean = 2.5; deviations = |1-2.5|+|2-2.5|+|3-2.5|+|4-2.5| = 1.5+0.5+0.5+1.5 = 4.0; MAD = 4.0/4 = 1.0.
    Fault hypothesis: If the function returns the variance instead of MAD, we'd get 1.25 (not 1.0).
    """
    result = _case0_mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert result == 1.0

from solution import mean_absolute_deviation as _case1_mean_absolute_deviation

def test_single_element():
    """A single-element list has zero deviation from its own mean.

    Contract quote: "Mean Absolute Deviation is the average absolute difference between each element and a centerpoint (mean in this case)"
    Input domain: A list containing exactly one float.
    Expected result: The only element equals the mean, so every |x - mean| = 0, hence MAD = 0.
    Fault hypothesis: Off-by-one in length handling could produce NaN or incorrect division.
    """
    result = _case1_mean_absolute_deviation([42.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case2_mean_absolute_deviation

def test_all_identical_elements():
    """When all elements are identical, MAD must be zero.

    Contract quote: "MAD = average | x - x_mean |"
    Input domain: A list of three identical floats.
    Expected result: Every element equals the mean, so all deviations are 0, MAD = 0.
    Fault hypothesis: Floating-point accumulation error might produce a tiny non-zero value.
    """
    result = _case2_mean_absolute_deviation([7.0, 7.0, 7.0, 7.0])
    assert result == 0.0

from solution import mean_absolute_deviation as _case3_mean_absolute_deviation

def test_negative_and_positive_numbers():
    """MAD should be symmetric with respect to sign changes.

    Contract quote: "MAD = average | x - x_mean |"
    Input domain: [-1.0, 0.0, 1.0].
    Expected result: mean = 0; deviations = 1 + 0 + 1 = 2; MAD = 2/3 ≈ 0.666666...
    Fault hypothesis: Sign errors in computing deviations could flip signs before abs().
    """
    result = _case3_mean_absolute_deviation([-1.0, 0.0, 1.0])
    expected = 2.0 / 3.0
    assert abs(result - expected) < 1e-12

from solution import mean_absolute_deviation as _case4_mean_absolute_deviation

def test_two_elements():
    """For two values, MAD is half their absolute difference.

    Contract quote: "MAD = average | x - x_mean |"
    Input domain: [10.0, 20.0].
    Expected result: mean = 15; deviations = 5 + 5 = 10; MAD = 10/2 = 5.0.
    Fault hypothesis: Using n-1 denominator (sample std dev style) would give 10/1 = 10.
    """
    result = _case4_mean_absolute_deviation([10.0, 20.0])
    assert result == 5.0

from solution import mean_absolute_deviation as _case5_mean_absolute_deviation

def test_return_type_is_float():
    """The function must always return a float, even when the mathematical result is an integer.

    Contract quote: "For a given list of input numbers, calculate Mean Absolute Deviation"
    Input domain: [1.0, 3.0].
    Expected result: mean = 2; deviations = 1 + 1 = 2; MAD = 1.0 which is a Python float.
    Fault hypothesis: Returning an int (e.g., via integer division //) would violate the contract.
    """
    result = _case5_mean_absolute_deviation([1.0, 3.0])
    assert isinstance(result, float)
    assert result == 1.0
