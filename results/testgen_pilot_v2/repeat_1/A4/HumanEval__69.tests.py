# Accepted by submit_tests; explanations in testgen_report.json.

def test_docstring_example_1():
    from solution import search
    assert search([4, 1, 2, 2, 3, 1]) == 2

def test_docstring_example_2():
    from solution import search
    assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

def test_docstring_example_3():
    from solution import search
    assert search([5, 5, 4, 4, 4]) == -1

def test_single_element_exact_match():
    from solution import search
    assert search([1]) == 1

def test_single_element_no_match():
    from solution import search
    assert search([2]) == -1

def test_boundary_freq_equals_value():
    from solution import search
    assert search([3, 3, 3]) == 3
