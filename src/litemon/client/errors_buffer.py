import time
from threading import Lock
from typing import Dict, Any, List

_errors_buffer = Dict[str, Dict[str, Any]] = {}
_lock = Lock()
MAX_ERRORS = 10


def record_error(func_name: str, error_type: str) -> None:
    """
    Records an error event in the local client-side error buffer.

    Args:
        func_name (str): Nameof the monitored function.
        error_type (str): Type or class name of the error.
    """
    entry = {
        "error": error_type,
        "timestamp": time.time()
    }

    with _lock:
        if func_name not in _errors_buffer:
            _errors_buffer[func_name] = []
        _errors_buffer[func_name].append(entry)

        # Trim to max allowed errors per function
        _errors_buffer[func_name] = _errors_buffer[func_name][-MAX_ERRORS:]


def get_errors() -> Dict[str, Dict[str,Any]]:
    """
    Returns a snapshot of the current errors buffer.

    Returns:
        dict: Function names mapped to lists of error entries.
    """

    with _lock:
        return dict(_errors_buffer)


def reset_errors() -> None:
    """
    Clears the local error buffer.
    """
    with _lock:
        _errors_buffer.clear()


def fetch_and_clear_errors() -> Dict[str, List[Dict[str,Any]]]:
    """
    Fetches all collected errors and clears the local buffer.
    Used by the client to push errors to the LiteMon server.

    Returns:
        dict: A snapshot of errors collected so far.
    """
    global _errors_buffer
    with _lock:
        snapshot = dict(_errors_buffer) # Copy current errors
        _errors_buffer.clear() # Reset buffer after fetching
        return snapshot