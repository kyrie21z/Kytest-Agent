# Accepted by submit_tests; explanations in testgen_report.json.

def test_docstring_example():
    """Verify the doctest example: [1,2,3,4] has MAD = 1.0.
    mean = 2.5; deviations: |1-2.5|+|2-2.5|+|3-2.5|+|4-2.5| = 1.5+0.5+0.5+1.5 = 4.0;
    MAD = 4.0/4 = 1.0."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert abs(result - 1.0) < 1e-09

def test_single_element_zero_mad():
    """A single-element list has zero deviation from its own mean.
    mean = x, |x - x| = 0, MAD = 0."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([42.0])
    assert result == 0.0

def test_all_identical_values():
    """When all elements are equal, every deviation from the mean is 0,
    so MAD must be 0 regardless of how many elements there are."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([7.0, 7.0, 7.0, 7.0, 7.0])
    assert result == 0.0

def test_negative_numbers():
    """[-1, 0, 1]: mean = 0; |−1−0|+|0−0|+|1−0| = 2; MAD = 2/3."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([-1.0, 0.0, 1.0])
    expected = 2.0 / 3.0
    assert abs(result - expected) < 1e-09

def test_two_elements_symmetric():
    """[0, 10]: mean = 5; |0-5|+|10-5| = 5+5 = 10; MAD = 10/2 = 5."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([0.0, 10.0])
    assert abs(result - 5.0) < 1e-09

def test_return_type_is_float():
    """The function must return a float, not an int, even when the result
    is a whole number like 1.0."""
    from solution import mean_absolute_deviation
    result = mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    assert isinstance(result, float)
