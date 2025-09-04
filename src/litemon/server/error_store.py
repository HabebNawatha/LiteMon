from collections import defaultdict
import time
from typing import Dict, List

_error_logs = defaultdict(list)
MAX_ERROR = 10


def store_errors(errors: Dict[str, List[Dict]]) -> None:
    """
    Merges incoming errors into the central store.
    """
    for func_name, entries in errors.items():
        if not isinstance(entries, list):
            continue

        for entry in entries:
            error_type = entry.get("error")
            args = entry.get("args")
            kwargs = entry.get("kwargs")
            if error_type:
                record_error(func_name, error_type, args, kwargs)


def record_error(func_name, error_type, args=None, kwargs=None):
    print("Args:", args)
    print("kwargs:", kwargs)
    _error_logs[func_name].append(
        {
            "error": error_type,
            "timestamp": time.time(),
            "args": args or [],
            "kwargs": kwargs or {},
        }
    )

    _error_logs[func_name] = _error_logs[func_name][-MAX_ERROR:]


def get_all_errors() -> Dict[str, List[Dict]]:
    return dict(_error_logs)


def reset_errors():
    _error_logs.clear()
