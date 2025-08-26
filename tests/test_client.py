import time
import requests
import pytest
from unittest.mock import MagicMock
from litemon.client import configure_client, stop_client, push_metrics
from litemon.client.metrics_buffer import record_call


@pytest.fixture(autouse=True)
def cleanup_client():
    # Ensure client threads are stopped after each test
    stop_client()
    yield
    stop_client()


def test_client_pushes_metrics_successfully(monkeypatch):
    pushed_data = {}

    def mock_post(url, json, timeout):
        pushed_data.update(json)
        return MagicMock(status_code=200)

    monkeypatch.setattr(requests, "post", mock_post)

    # Record a metric
    record_call("func_ok", success=True, duration=0.1)

    # Start client but don't rely on async thread timing
    configure_client(server_url="http://127.0.0.1:6400", push_interval=5)

    # Manually trigger a synchronous push
    push_metrics()

    stop_client()
    assert "func_ok" in pushed_data


def test_client_handles_push_failure(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *a, **k: MagicMock(status_code=500))
    record_call("func_fail", success=True, duration=0.2)

    configure_client(server_url="http://127.0.0.1:6400", push_interval=0.1)
    time.sleep(0.2)
    stop_client()


def test_client_handles_request_exception(monkeypatch):
    monkeypatch.setattr(
        requests,
        "post",
        lambda *a, **k: (_ for _ in ()).throw(requests.RequestException("boom")),
    )
    record_call("func_err", success=True, duration=0.3)

    configure_client(server_url="http://127.0.0.1:6400", push_interval=0.1)
    time.sleep(0.2)
    stop_client()
