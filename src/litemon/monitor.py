import time
from functools import wraps
from .metrics import record_call


def monitor(func):
    """
    A lightweight decorator to monitor function calls.

    Tracks:
    - Total calls
    - Successses vs failures
    - Average execution time

    Example:
        @monitor
        def greet(name):
            return f"Hello, {name}!"
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            record_call(func.__name__, success=True, duration=duration)
            return result
        except Exception:
            duration = time.perf_counter() - start
            record_call(func.__name__, success=False, duration=duration)
            raise

    return wrapper
