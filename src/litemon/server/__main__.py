import argparse
from .app import run_server


def main():
    parser = argparse.ArgumentParser(description="LiteMon metrics server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=6400, help="Server port")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
