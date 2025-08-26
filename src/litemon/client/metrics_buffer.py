from threading import Lock
from typing import Dict, Any

# In-memory buffer for client-side metrics before pushing to the server
_metrics_buffer: Dict[str, Dict[str, Any]] = {}
_lock = Lock()


def record_call(func_name: str, success: bool = True, duration: float = 0.0) -> None:
    """
    Records a function call locally in the client's metrics buffer.

    Args:
        func_name (str): Name of the monitored function.
        success (bool): Whether the call succeeded.
        duration (float): Execution time in seconds.
    """
    with _lock:
        if func_name not in _metrics_buffer:
            _metrics_buffer[func_name] = {
                "calls": 0,
                "success": 0,
                "failures": 0,
                "avg_time": 0.0,
            }

        metrics = _metrics_buffer[func_name]
        metrics["calls"] += 1
        if success:
            metrics["success"] += 1
        else:
            metrics["failures"] += 1

        # Update average execution time incrementally
        metrics["avg_time"] = (
            metrics["avg_time"] * (metrics["calls"] - 1) + duration
        ) / metrics["calls"]


def get_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Returns a snapshot of the current metrics buffer.

    Returns:
        dict: Function names mapped to their statistics.
    """
    with _lock:
        return dict(_metrics_buffer)


def reset_metrics() -> None:
    """
    Clears the local metrics buffer.
    """
    with _lock:
        _metrics_buffer.clear()


def fetch_and_clear() -> Dict[str, Dict[str, Any]]:
    """
    Fetches all collected metrics and clears the local buffer.
    Used by the client to push metrics to the LiteMon server.

    Returns:
        dict: A snapshot of metrics collected so far.
    """
    global _metrics_buffer
    with _lock:
        snapshot = dict(_metrics_buffer)  # Copy current metrics
        _metrics_buffer.clear()  # Reset buffer after fetching
        return snapshot
