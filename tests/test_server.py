import threading
import requests
from litemon.server.app import run_server
import subprocess
import sys
import time
import socket


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_test_server(port=6500):
    """Start the LiteMon server in a background thread for testing."""
    # If server is already running, just reuse it
    if is_port_in_use(port):
        return None

    def run():
        run_server(host="127.0.0.1", port=port)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    # Give server time to start
    time.sleep(0.5)
    return thread


def test_metrics_and_push_and_reset():
    start_test_server(port=6500)
    base = "http://127.0.0.1:6500"

    metrics = {"func_ok": {"calls": 1, "success": 1, "failures": 0, "avg_time": 0.1}}
    res = requests.post(f"{base}/push", json=metrics)
    assert res.status_code == 200


def test_invalid_json_returns_400():
    start_test_server(port=6500)
    base = "http://127.0.0.1:6500"

    res = requests.post(f"{base}/push", data="invalid-json")
    assert res.status_code == 400


def test_metrics_endpoint_returns_valid_json():
    """Integration test: push metrics and fetch them from /metrics endpoint."""
    start_test_server(port=6500)
    base = "http://127.0.0.1:6500"

    # Push metrics
    metrics = {"test_func": {"calls": 1, "success": 1, "failures": 0, "avg_time": 0.5}}
    res = requests.post(f"{base}/push", json=metrics)
    assert res.status_code == 200

    # Fetch them
    response = requests.get(f"{base}/metrics")
    assert response.status_code == 200

    data = response.json()
    assert "test_func" in data
    assert data["test_func"]["calls"] == 1


def test_multiple_clients_push_concurrently():
    """Simulate 5 clients pushing metrics at the same time."""
    start_test_server(port=6500)
    base = "http://127.0.0.1:6500"

    def push_metrics(name):
        metrics = {name: {"calls": 1, "success": 1, "failures": 0, "avg_time": 0.1}}
        requests.post(f"{base}/push", json=metrics)

    threads = [
        threading.Thread(target=push_metrics, args=(f"func{i}",)) for i in range(5)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    res = requests.get(f"{base}/metrics")
    assert res.status_code == 200
    data = res.json()
    assert all(f"func{i}" in data for i in range(5))


def test_cli_entrypoint_runs_help():
    """Ensure CLI entrypoint works with --help flag."""
    result = subprocess.run(
        [sys.executable, "-m", "litemon.server", "--help"],
        capture_output=True,
        text=True,
    )
    assert "LiteMon metrics server" in result.stdout
    assert result.returncode == 0
