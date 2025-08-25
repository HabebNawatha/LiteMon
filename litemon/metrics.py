from threading import Lock
from typing import Dict, Any


# In-memory metrics registry
_metrics: Dict[str, Dict[str, Any]] = {}
_lock = Lock()

def record_call(func_name: str, success: bool = True, duration: float = 0.0) -> None:
    """
    Records a function call in the metrics registry.

    Args:
        func_name (str): Name of the function being monitored.
        success (bool): Whether the function executed successfully.
        duration (float): Execution time in seconds.
    """
    with _lock:
        if func_name not in _metrics:
            _metrics[func_name] = {
                "calls": 0,
                "success": 0,
                "failures": 0,
                "avg_time": 0.0
            }

            metrics = _metrics[func_name]
            metrics["calls"] += 1
            if success:
                metrics["success"] += 1
            else:
                metrics["failures"] += 1

            # Update average execution time incrementally
            metrics["avg_time"] = (
                (metrics["avg_time"] * (metrics["calls"] - 1) + duration) / metrics["calls"]
            )

def get_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Returns the current metrics snapshot.

    Returns:
        dict: A dictionary containing function names and their statistics.
    """
    with _lock:
        # Return a copy to avoid accidental mutation
        return dict(_metrics)
    
def reset_metrics() -> None:
    """
    Clears all collected metrics
    """
    with _lock:
        _metrics.clear()