#!/usr/bin/env python3
"""serve.py — Local development server for the-backtest-that-lied. Zero dependencies."""
import http.server, os, signal, socket, sys

PORT = 8000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)
    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

def main():
    try:
        with http.server.HTTPServer(("127.0.0.1", PORT), Handler) as httpd:
            print(f"\n  The Backtest That Lied")
            print(f"  Serving from: {ROOT}")
            print(f"  URL: http://127.0.0.1:{PORT}\n")
            def shutdown(sig, frame):
                print("\nShutting down.")
                httpd.shutdown()
            signal.signal(signal.SIGINT, shutdown)
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:
            print(f"Port {PORT} is in use. Try: python scripts/serve.py")
        else:
            print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
