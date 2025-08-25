import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from .metrics import get_metrics


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            metrics = get_metrics()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(metrics, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")


def start_dashboard(port: int = 8000):
    """
    Starts a lightweight dashboard server in a background thread.

    Args:
        port (int): Port number for the dashboard (default: 8000)
    """

    def run():
        server = HTTPServer(("127.0.0.1", port), MetricsHandler)
        print(f"📊 LiteMon dashboard running at http://127.0.0.1:{port}/metrics")
        server.serve_forever()

    thread = Thread(target=run, daemon=True)
    thread.start()
