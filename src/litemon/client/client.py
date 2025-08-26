import threading
import time
import requests
from typing import Optional
from .metrics_buffer import fetch_and_clear

# Default LiteMon server URL — users can override via start_client()
_server_url: Optional[str] = None
_push_interval: Optional[int] = None
_stop_event = threading.Event()
_thread: Optional[threading.Thread] = None


def push_metrics():
    """
    Immediately pushes any buffered metrics to the LiteMon server.
    Useful for tests or manual flushes.
    """
    metrics = fetch_and_clear()
    if not metrics or not _server_url:
        return

    try:
        res = requests.post(f"{_server_url}/push", json=metrics, timeout=2)
        if res.status_code != 200:
            print(f"⚠️ LiteMon: Failed to push metrics ({res.status_code})")
    except requests.RequestException as e:
        print(f"⚠️ LiteMon: Error pushing metrics: {e}")


def _push_metrics_periodically():
    """
    Background thread that periodically pushes metrics to the LiteMon server.
    """
    global _server_url

    while not _stop_event.is_set():
        metrics = fetch_and_clear()
        if metrics and _server_url:
            try:
                res = requests.post(f"{_server_url}/push", json=metrics, timeout=2)
                if res.status_code != 200:
                    print(f"⚠️ LiteMon: Failed to push metrics ({res.status_code})")
            except requests.RequestException as e:
                print(f"⚠️ LiteMon: Error pushing metrics: {e}")
        time.sleep(_push_interval or 5)


def configure_client(server_url: str = "http://127.0.0.1:6400", push_interval: int = 5):
    """
    Starts the LiteMon client to periodically push metrics.

    Args:
        server_url (str): LiteMon server URL.
        push_interval (int): How often to push metrics (seconds).
    """
    global _server_url, _push_interval, _thread

    _server_url = server_url
    _push_interval = push_interval

    # Start pushing in background thread if not already running
    if not _thread or not _thread.is_alive():
        _thread = threading.Thread(target=_push_metrics_periodically, daemon=True)
        _thread.start()


def stop_client():
    """Stops the LiteMon client."""
    _stop_event.set()
    if _thread and _thread.is_alive():
        _thread.join()
