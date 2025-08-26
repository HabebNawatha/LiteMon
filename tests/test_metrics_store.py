from litemon.server.metrics_store import store_metrics, get_all_metrics


def test_store_and_merge_metrics():
    store_metrics({"f1": {"calls": 1, "success": 1, "failures": 0, "avg_time": 0.2}})
    store_metrics({"f1": {"calls": 1, "success": 0, "failures": 1, "avg_time": 0.4}})
    metrics = get_all_metrics()["f1"]

    assert metrics["calls"] == 2
    assert metrics["success"] == 1
    assert metrics["failures"] == 1
    assert 0.2 <= metrics["avg_time"] <= 0.4
