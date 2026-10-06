# Accepted by submit_tests; explanations in testgen_report.json.

import math as _case0_math

def test_docstring_example():
    """Verify the exact example from the docstring: [1.0, 2.0, 3.0, 4.0] -> 1.0.
    
    Contract quote: ">>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0"
    
    Input domain: A list of four consecutive integers starting at 1.
    
    Expected result derivation:
      mean = (1+2+3+4)/4 = 2.5
      deviations = |1-2.5| + |2-2.5| + |3-2.5| + |4-2.5| = 1.5 + 0.5 + 0.5 + 1.5 = 4.0
      MAD = 4.0 / 4 = 1.0
    
    Faulty behavior detected: Incorrect mean calculation, wrong MAD formula,
    or any arithmetic error producing a non-1.0 result.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert result == 1.0

def test_single_element_returns_zero():
    """A single-element list has zero deviation because the element equals the mean.
    
    Contract quote: "Mean Absolute Deviation is the average absolute difference between
    each element and a centerpoint (mean in this case)"
    
    Input domain: A list containing exactly one numeric value.
    
    Expected result derivation:
      For [x], mean = x, so |x - x| = 0, and MAD = 0 / 1 = 0.0.
    
    Faulty behavior detected: Division-by-zero crash, or returning a non-zero value
    for a singleton list where all deviations are trivially zero.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([42.0])
    assert result == 0.0

def test_two_elements_symmetric():
    """Two elements equidistant from their mean yield MAD equal to half their distance.
    
    Contract quote: "MAD = average | x - x_mean |"
    
    Input domain: A list of two numbers symmetric around their midpoint, e.g., [-3.0, 3.0].
    
    Expected result derivation:
      mean = (-3 + 3) / 2 = 0.0
      deviations = |-3 - 0| + |3 - 0| = 3 + 3 = 6
      MAD = 6 / 2 = 3.0
    
    Faulty behavior detected: Wrong mean computation for even-length lists,
    or incorrect absolute-difference summation.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([-3.0, 3.0])
    assert result == 3.0

def test_all_identical_values():
    """When every element is the same, MAD must be exactly zero.
    
    Contract quote: "average absolute difference between each element and a centerpoint"
    
    Input domain: A list where all elements share the same value, e.g., [7.0, 7.0, 7.0, 7.0].
    
    Expected result derivation:
      mean = 7.0, every |x - mean| = 0, so MAD = 0 / 4 = 0.0.
    
    Faulty behavior detected: Failure to handle uniform datasets; any non-zero result
    indicates a bug in the absolute-difference loop or mean calculation.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([7.0, 7.0, 7.0, 7.0])
    assert result == 0.0

import math as _case4_math

def test_negative_numbers():
    """MAD should be unaffected by negative values; absolute differences handle signs.
    
    Contract quote: "average absolute difference between each element and a centerpoint"
    
    Input domain: A list with mixed-sign values, e.g., [-2.0, 0.0, 2.0].
    
    Expected result derivation:
      mean = (-2 + 0 + 2) / 3 = 0.0
      deviations = |-2 - 0| + |0 - 0| + |2 - 0| = 2 + 0 + 2 = 4
      MAD = 4 / 3 ≈ 1.3333...
    
    Faulty behavior detected: Sign errors in subtraction before abs(), or incorrect
    handling of negative operands in the mean calculation.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([-2.0, 0.0, 2.0])
    expected = 4.0 / 3.0
    assert _case4_math.isclose(result, expected, rel_tol=1e-09)

def test_return_type_is_float():
    """The function must return a float, not an int, per its signature.
    
    Contract quote: "Mean Absolute Deviation is the average absolute difference between
    each element and a centerpoint (mean in this case):"
    
    Input domain: Any valid non-empty list of floats, e.g., [1.0, 2.0].
    
    Expected result derivation:
      The return annotation specifies float. Even when the mathematical result
      is an integer (like 0.5 rounded), Python's division always produces float.
      We verify the returned object is an instance of float.
    
    Faulty behavior detected: Returning an int (e.g., via integer division // or
    explicit int() cast), which would violate the type contract.
    """
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([1.0, 2.0])
    assert isinstance(result, float)
