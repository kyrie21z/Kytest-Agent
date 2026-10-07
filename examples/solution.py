def classify(value, low, high):
    """For low <= high, return -1 below low, 1 above high, and 0 inside the inclusive interval."""
    if value < low:
        return -1
    if value > high:
        return 1
    return 0
