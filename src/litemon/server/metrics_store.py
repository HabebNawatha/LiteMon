from threading import Lock
from typing import Dict, Any

_metrics_store: Dict[str, Dict[str, Any]] = {}
_lock = Lock()


def store_metrics(new_metrics: Dict[str, Dict[str, Any]]):
    """Merges incoming metrics into the central store."""
    with _lock:
        for func, stats in new_metrics.items():
            if func not in _metrics_store:
                _metrics_store[func] = stats
            else:
                existing = _metrics_store[func]
                existing["calls"] += stats.get("calls", 0)
                existing["success"] += stats.get("success", 0)
                existing["failures"] += stats.get("failures", 0)

                if stats.get("calls", 0) > 0:
                    total_time = (
                        existing["avg_time"] * existing["calls"]
                        + stats["avg_time"] * stats["calls"]
                    )
                    existing["avg_time"] = total_time / existing["calls"]


def get_all_metrics() -> Dict[str, Dict[str, Any]]:
    with _lock:
        return dict(_metrics_store)


def reset_metrics():
    with _lock:
        _metrics_store.clear()
