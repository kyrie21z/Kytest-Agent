# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    from solution import combinations_list
    result = combinations_list([])
    assert result == [[]]
    assert isinstance(result, list)
    assert len(result) == 1
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: An empty list []\n    oracle_reason: The base case explicitly states that an empty list returns [[]], i.e., a list containing exactly one element which is the empty subset.\n    fault_hypothesis: If the function incorrectly returns [] instead of [[]], or raises an error on empty input, this assertion will catch it.\n    "

def test_all_elements_present():
    from solution import combinations_list
    result = combinations_list([1, 2, 3])
    assert [3, 2, 1] in result
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A three-element list [1, 2, 3]\n    oracle_reason: The full set of all elements must be one of the combinations. Due to the recursive implementation where the head is appended to each tail combination, the full set appears in reverse order: [3, 2, 1].\n    fault_hypothesis: If the function fails to include the complete set of all elements, this assertion will detect it.\n    "

def test_single_element():
    from solution import combinations_list
    result = combinations_list([1])
    assert result == [[], [1]]
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A single-element list [1]\n    oracle_reason: Base case gives [[]]. Recursive step iterates over el=[], producing [] and [1]. So result is exactly [[], [1]].\n    fault_hypothesis: If the function returns wrong subsets (e.g., missing [], or returning [[1]] only), this exact equality check catches it.\n    "

def test_two_elements_exact():
    from solution import combinations_list
    result = combinations_list([1, 2])
    assert result == [[], [1], [2], [2, 1]]
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A two-element list [1, 2]\n    oracle_reason: Recursive call on [2] yields [[], [2]]. For el=[], we get [] and [1]. For el=[2], we get [2] and [2, 1]. Concatenated in order: [[], [1], [2], [2, 1]].\n    fault_hypothesis: Wrong ordering, missing subset, or extra subset would cause this exact match to fail.\n    "

def test_duplicate_elements():
    from solution import combinations_list
    result = combinations_list([1, 1])
    assert result == [[], [1], [1], [1, 1]]
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A list with duplicate elements [1, 1]\n    oracle_reason: The function treats each position independently. combinations_list([1]) -> [[], [1]]. Then el=[] gives [], [1]; el=[1] gives [1], [1, 1]. Result: [[], [1], [1], [1, 1]]. Note there are two [1] entries.\n    fault_hypothesis: If the function deduplicates results (as a set-based approach might), it would miss one of the [1] entries, causing this exact match to fail.\n    "

def test_four_elements_count():
    from solution import combinations_list
    result = combinations_list([1, 2, 3, 4])
    assert len(result) == 16
    assert [] in result
    assert [4, 3, 2, 1] in result
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A four-element list [1, 2, 3, 4]\n    oracle_reason: For n=4, there must be exactly 2^4=16 subsets. The empty set [] is always present. The full set appears as [4, 3, 2, 1] due to the recursive head-appending pattern.\n    fault_hypothesis: If the function produces incorrect number of subsets (e.g., due to off-by-one error) or fails to include the complete set, these assertions catch it.\n    "

def test_three_elements_exact():
    from solution import combinations_list
    result = combinations_list([1, 2, 3])
    assert result == [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1]]
    "\n    contract_quote: 'Write a function to find all possible combinations of the elements of a given list.'\n    input_domain: A three-element list [1, 2, 3]\n    oracle_reason: Recursive trace: combinations_list([3])->[[[], [3]]. combinations_list([2,3]) iterates over [[], [3]], producing [[], [2], [3], [3, 2]]. Then combinations_list([1,2,3]) iterates over that, producing [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1]].\n    fault_hypothesis: Wrong ordering, missing subset, or incorrect element arrangement within subsets will cause this exact equality to fail.\n    "
