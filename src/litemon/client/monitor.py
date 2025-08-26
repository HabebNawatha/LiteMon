import time
import functools
from .metrics_buffer import record_call


def monitor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        success = True
        try:
            return func(*args, **kwargs)
        except Exception:
            success = False
            raise
        finally:
            duration = time.perf_counter() - start
            # Only record locally, don't push here
            record_call(func.__name__, success=success, duration=duration)

    return wrapper
