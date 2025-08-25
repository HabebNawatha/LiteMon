from unittest.mock import patch
import pytest
from litemon.metrics import reset_metrics, get_metrics
from litemon.monitor import monitor


def test_monitor_successful_function():
    """Ensure that the monitor decorator tracks successful calls."""
    reset_metrics()

    @monitor
    def greet(name):
        return f"Hello, {name}"

    result = greet("LiteMon")
    assert result == "Hello, LiteMon"

    metrics = get_metrics()["greet"]
    assert metrics["calls"] == 1
    assert metrics["success"] == 1
    assert metrics["failures"] == 0
    assert metrics["avg_time"] >= 0  # Execution time should be recorded


def test_monitor_failed_function():
    """Ensure that exceptions are recorded as failures but still raised."""
    reset_metrics()

    @monitor
    def fail_func():
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError):
        fail_func()

    metrics = get_metrics()["fail_func"]
    assert metrics["calls"] == 1
    assert metrics["success"] == 0
    assert metrics["failures"] == 1


def test_monitor_multiple_calls_and_durations():
    reset_metrics()

    @monitor
    def slow_func(delay):
        return delay

    with patch("time.perf_counter", side_effect=[0, 0.1, 1, 1.3]):
        slow_func(0.1)
        slow_func(0.3)

    metrics = get_metrics()["slow_func"]
    assert metrics["calls"] == 2
    assert metrics["success"] == 2
    assert metrics["avg_time"] == pytest.approx((0.1 + 0.3) / 2)


def test_monitor_multiple_functions():
    """Ensure that metrics are tracked separately for multiple monitored functions."""
    reset_metrics()

    @monitor
    def func_a():
        return "A"

    @monitor
    def func_b():
        return "B"

    func_a()
    func_a()
    func_b()

    metrics = get_metrics()
    assert metrics["func_a"]["calls"] == 2
    assert metrics["func_b"]["calls"] == 1


def test_monitor_preserves_function_metadata():
    """Ensure the monitor decorator preserves the original function name and docstring."""
    reset_metrics()

    @monitor
    def my_func():
        """This is my test function"""
        return 42

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "This is my test function"
    assert my_func() == 42
