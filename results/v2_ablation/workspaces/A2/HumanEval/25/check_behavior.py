from solution import factorize
import traceback

# Test negative input
try:
    result = factorize(-5)
    print('factorize(-5) returned:', repr(result))
except Exception as e:
    print('factorize(-5) raised:', type(e).__name__, str(e))

# Test float input
try:
    result = factorize(3.5)
    print('factorize(3.5) returned:', repr(result))
except Exception as e:
    print('factorize(3.5) raised:', type(e).__name__, str(e))

# Test zero
try:
    result = factorize(0)
    print('factorize(0) returned:', repr(result))
except Exception as e:
    print('factorize(0) raised:', type(e).__name__, str(e))

# Test one
try:
    result = factorize(1)
    print('factorize(1) returned:', repr(result))
except Exception as e:
    print('factorize(1) raised:', type(e).__name__, str(e))
