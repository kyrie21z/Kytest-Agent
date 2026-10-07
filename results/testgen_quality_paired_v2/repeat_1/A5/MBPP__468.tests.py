# Accepted by submit_tests; explanations in testgen_report.json.

def test_simple_increasing():
    """Test basic increasing sequence [1, 2, 3].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [1, 2, 3], a strictly increasing array of positive ints.

    Oracle: The entire array is an increasing subsequence. Product = 1*2*3 = 6.
    No shorter subsequence can exceed this since all elements > 1.
    Expected result: 6.

    Fault hypothesis: If the function fails to extend across the full sequence
    or miscalculates the product, it would return a value != 6.
    """
    from solution import max_product
    result = max_product([1, 2, 3])
    assert result == 6

def test_decreasing_sequence():
    """Test a strictly decreasing sequence [5, 4, 3, 2, 1].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [5, 4, 3, 2, 1], strictly decreasing positive ints.

    Oracle: No pair forms an increasing subsequence of length >= 2. Each
    individual element is a valid increasing subsequence of length 1.
    The maximum single element is 5. Expected result: 5.

    Fault hypothesis: If the function incorrectly combines non-increasing
    elements or picks the wrong single element, result != 5.
    """
    from solution import max_product
    result = max_product([5, 4, 3, 2, 1])
    assert result == 5

def test_single_element():
    """Test a single-element array [7].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [7], one positive integer.

    Oracle: The only increasing subsequence is [7] itself. Product = 7.
    Expected result: 7.

    Fault hypothesis: Off-by-one or initialization bugs could return wrong value.
    """
    from solution import max_product
    result = max_product([7])
    assert result == 7

def test_mixed_with_peak_subsequence():
    """Test [5, 2, 3, 4] where the best increasing subsequence is [2, 3, 4].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [5, 2, 3, 4], mixed positive integers.

    Oracle: Contiguous increasing subsequences: [5], [2, 3, 4]. Products:
    5 and 2*3*4=24. Max = 24. Expected result: 24.

    Fault hypothesis: If the function misses the subsequence starting at index 1,
    or miscalculates the product, result != 24.
    """
    from solution import max_product
    result = max_product([5, 2, 3, 4])
    assert result == 24

def test_negative_numbers():
    """Test with negative numbers [-3, -2, -1].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [-3, -2, -1], strictly increasing negative integers.

    Oracle: The full array is increasing. Products of contiguous increasing
    subsequences: [-3], [-2], [-1], [-3,-2]=6, [-2,-1]=2, [-3,-2,-1]=-6.
    Maximum product = 6. Expected result: 6.

    Fault hypothesis: Sign errors or incorrect product accumulation would
    yield a different result.
    """
    from solution import max_product
    result = max_product([-3, -2, -1])
    assert result == 6

def test_equal_elements_non_decreasing():
    """Test with equal elements [3, 3, 3].

    Contract quote: 'Write a function to find the maximum product formed by
    multiplying numbers of an increasing subsequence of that array.'

    Input domain: arr = [3, 3, 3], all equal positive integers.

    Oracle: The code uses `arr[j-1] > arr[j]` to break, so equal elements
    do NOT trigger a break. The full sequence [3,3,3] is treated as valid.
    Product = 3*3*3 = 27. Expected result: 27.

    Fault hypothesis: If the function treats equal elements as breaking the
    increasing property (strictly increasing interpretation), it might return 3.
    """
    from solution import max_product
    result = max_product([3, 3, 3])
    assert result == 27
