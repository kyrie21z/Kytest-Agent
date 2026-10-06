from solution import factorize
try:
    result = factorize(None)
    print('factorize(None) returned:', repr(result))
except Exception as e:
    print('factorize(None) raised:', type(e).__name__, str(e))
