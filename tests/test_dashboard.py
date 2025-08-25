import time
import socket
import requests
import pytest
from litemon.dashboard import start_dashboard
from litemon.metrics import reset_metrics, record_call


def get_free_port():
    """Find an available free port on localhost for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture
def dashboard_server():
    """Start the dashboard on a free port and wait for it to be ready."""
    port = get_free_port()
    start_dashboard(port=port)
    time.sleep(0.2)  # Give server a moment to start
    return f"http://127.0.0.1:{port}"


def test_metrics_endpoint_returns_valid_json(dashboard_server):
    reset_metrics()
    record_call("test_func", success=True, duration=0.5)

    url = f"{dashboard_server}/metrics"
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()
    assert "test_func" in data
    assert data["test_func"]["calls"] == 1


def test_metrics_endpoint_404_for_invalid_path(dashboard_server):
    url = f"{dashboard_server}/invalid"
    response = requests.get(url)
    assert response.status_code == 404
