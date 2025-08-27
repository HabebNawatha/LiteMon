import time
import functools
import inspect
from .metrics_buffer import record_call


def monitor(func):
    is_async = inspect.iscoroutinefunction(func)

    if is_async:
        # Async wrapper
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            success = True
            try:
                return await func(*args, **kwargs)
            except Exception:
                success = False
                raise
            finally:
                duration = time.perf_counter() - start
                record_call(func.__name__, success=success, duration=duration)

        return async_wrapper

    else:
        # Sync wrapper
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            success = True
            try:
                return func(*args, **kwargs)
            except Exception:
                success = False
                raise
            finally:
                duration = time.perf_counter() - start
                record_call(func.__name__, success=success, duration=duration)

        return sync_wrapper
