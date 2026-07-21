from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import socket

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_PORT = int(os.environ.get("PORT", "8000"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def log_message(self, format, *args):
        print(f"[server] {self.address_string()} - - [{self.log_date_time_string()}] {format % args}")


def choose_port(start_port: int) -> int:
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise OSError("No available ports found in the range")


if __name__ == "__main__":
    port = choose_port(DEFAULT_PORT)
    with ThreadingHTTPServer(("127.0.0.1", port), Handler) as httpd:
        print(f"Serving {ROOT_DIR} at http://127.0.0.1:{port}")
        httpd.serve_forever()
