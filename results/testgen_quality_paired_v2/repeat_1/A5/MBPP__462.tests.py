# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_input():
    """Test that an empty list returns a list containing only the empty list."""
    from solution import combinations_list
    result = combinations_list([])
    assert result == [[]]
    assert isinstance(result, list)
    assert len(result) == 1

def test_single_element():
    """Test that a single-element list returns two combinations: empty and the element itself."""
    from solution import combinations_list
    result = combinations_list([42])
    assert isinstance(result, list)
    assert len(result) == 2
    assert [] in result
    assert [42] in result

def test_two_elements_count_and_content():
    """Test that a two-element list produces exactly 4 combinations covering all subsets."""
    from solution import combinations_list
    result = combinations_list([1, 2])
    assert isinstance(result, list)
    assert len(result) == 4
    assert [] in result
    assert [1] in result
    assert [2] in result
    assert [2, 1] in result

def test_power_of_two_length():
    """Test that the output length is always 2^n for an input of length n."""
    from solution import combinations_list
    for n in range(8):
        lst = list(range(n))
        result = combinations_list(lst)
        assert len(result) == 2 ** n, f'Expected {2 ** n} combinations for n={n}, got {len(result)}'

def test_all_subsets_present_three_elements():
    """Verify all 8 subsets of a 3-element list are present with correct content."""
    from solution import combinations_list
    result = combinations_list([1, 2, 3])
    assert len(result) == 8
    subset_sets = [frozenset(s) for s in result]
    expected = [frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2}), frozenset({3}), frozenset({1, 3}), frozenset({2, 3}), frozenset({1, 2, 3})]
    for exp in expected:
        assert exp in subset_sets, f'Missing subset {exp}'
    assert len(subset_sets) == len(expected)
