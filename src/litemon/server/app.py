import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from .metrics_store import store_metrics, get_all_metrics, reset_metrics


class LiteMonHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/metrics":
            self._send_json(get_all_metrics())
        else:
            self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/reset":
            reset_metrics()
            return self._send_json({"status": "reset"})

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return self._send_json({"error": "Invalid JSON"}, status=400)

        if parsed.path == "/push":
            if not isinstance(data, dict):
                return self._send_json({"error": "Expected metrics dict"}, status=400)
            store_metrics(data)
            self._send_json({"status": "ok"})
        else:
            self._send_json({"error": "Not found"}, status=404)


def run_server(host="127.0.0.1", port=6400):
    """Starts the LiteMon metrics server."""
    server = HTTPServer((host, port), LiteMonHandler)
    print(f"🚀 LiteMon server running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 LiteMon server stopped")
    finally:
        server.server_close()
