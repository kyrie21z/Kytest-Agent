# Accepted by submit_tests; explanations in testgen_report.json.

from solution import pancake_sort as _case0_pancake_sort

def test_empty_list():
    """An empty list should return an empty list.
    Contract quote: "Write a function to sort a list of elements." — an empty list is a valid list of zero elements.
    Input domain: []
    Oracle: Sorting zero elements yields zero elements.
    Fault hypothesis: Function might raise IndexError or return non-empty result for empty input."""
    result = _case0_pancake_sort([])
    assert result == []
    assert isinstance(result, list)

from solution import pancake_sort as _case1_pancake_sort

def test_single_element():
    """A single-element list should be returned unchanged.
    Contract quote: "Write a function to sort a list of elements." — one element is trivially sorted.
    Input domain: [42]
    Oracle: A list with one element is already sorted.
    Fault hypothesis: Function might modify or drop the single element."""
    result = _case1_pancake_sort([42])
    assert result == [42]
    assert isinstance(result, list)

from solution import pancake_sort as _case2_pancake_sort

def test_already_sorted():
    """An already sorted list should return the same sorted sequence.
    Contract quote: "Write a function to sort a list of elements." — output must be sorted ascending.
    Input domain: [1, 2, 3, 4, 5]
    Oracle: Output equals input because input is already sorted.
    Fault hypothesis: Function might reorder elements even when already sorted."""
    result = _case2_pancake_sort([1, 2, 3, 4, 5])
    assert result == [1, 2, 3, 4, 5]

from solution import pancake_sort as _case3_pancake_sort

def test_reverse_sorted():
    """A reverse-sorted list must be fully reversed to ascending order.
    Contract quote: "Write a function to sort a list of elements." — output must be ascending.
    Input domain: [5, 4, 3, 2, 1]
    Oracle: Output is [1, 2, 3, 4, 5].
    Fault hypothesis: Function fails to handle worst-case reversal scenario."""
    result = _case3_pancake_sort([5, 4, 3, 2, 1])
    assert result == [1, 2, 3, 4, 5]

from solution import pancake_sort as _case4_pancake_sort

def test_with_duplicates():
    """A list with duplicate elements must still be sorted correctly.
    Contract quote: "Write a function to sort a list of elements." — duplicates are valid elements.
    Input domain: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    Oracle: Output is [1, 1, 2, 3, 3, 4, 5, 5, 6, 9].
    Fault hypothesis: Function might lose duplicates or fail when max appears multiple times (index returns first occurrence)."""
    result = _case4_pancake_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
    assert len(result) == 10

from solution import pancake_sort as _case5_pancake_sort

def test_no_mutation_v2():
    """The function must not mutate the original list.
    Contract quote: "Write a function to sort a list of elements." — caller expects returned value to be sorted;
    side-effect-free behavior is expected unless documented otherwise.
    Input domain: [3, 1, 2]
    Oracle: Returned value is [1, 2, 3] AND original list remains [3, 1, 2].
    Fault hypothesis: Function mutates the input list in-place instead of returning a new sorted copy."""
    original = [3, 1, 2]
    result = _case5_pancake_sort(original)
    assert (result, original) == ([1, 2, 3], [3, 1, 2])
