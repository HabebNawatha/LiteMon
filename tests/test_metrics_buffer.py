import pytest
from litemon.client.metrics_buffer import (
    reset_metrics,
    record_call,
    get_metrics,
)


def test_metrics_tracking():
    reset_metrics()
    assert get_metrics() == {}

    record_call("test_func", success=True, duration=0.5)
    metrics = get_metrics()

    assert "test_func" in metrics
    assert metrics["test_func"]["calls"] == 1
    assert metrics["test_func"]["success"] == 1
    assert metrics["test_func"]["failures"] == 0
    assert metrics["test_func"]["avg_time"] == 0.5

    reset_metrics()
    assert get_metrics() == {}


def test_multiple_calls_mixed_outcomes():
    reset_metrics()
    record_call("multi_func", success=True, duration=0.2)
    record_call("multi_func", success=False, duration=0.4)
    metrics = get_metrics()["multi_func"]

    assert metrics["calls"] == 2
    assert metrics["success"] == 1
    assert metrics["failures"] == 1
    assert metrics["avg_time"] == pytest.approx((0.2 + 0.4) / 2)


def test_multiple_functions():
    reset_metrics()
    record_call("func1", success=True, duration=0.1)
    record_call("func2", success=False, duration=0.3)

    metrics = get_metrics()
    assert "func1" in metrics
    assert "func2" in metrics
    assert metrics["func1"]["success"] == 1
    assert metrics["func2"]["failures"] == 1


def test_avg_time_calculation():
    reset_metrics()
    record_call("timed_func", success=True, duration=0.1)
    record_call("timed_func", success=True, duration=0.3)

    metrics = get_metrics()["timed_func"]
    assert metrics["avg_time"] == pytest.approx(0.2)


def test_reset_is_idempotent():
    reset_metrics()
    reset_metrics()
    assert get_metrics() == {}
