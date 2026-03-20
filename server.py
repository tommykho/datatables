"""
Simple HTTP server for the datatables viewer.
Serves the current directory at http://localhost:8000/

Extra endpoint:
  GET /api/files  — returns a JSON array of all .csv and .xlsx filenames
                    in the served directory, sorted alphabetically.
                    Used by the browser-side folder scan in index.html.

Press Ctrl+C to stop.
"""
import http.server
import json
import os
import sys
import threading
import time

PORT = 8000


class FilesAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Like SimpleHTTPRequestHandler but adds GET /api/files.

    The browser calls fetch('/api/files') to discover available CSV/XLSX files.
    All other requests (including GET /) fall through to the base class, so
    index.html is served normally at http://localhost:8000/.
    """

    def do_GET(self):
        if self.path == '/api/files':
            self._serve_files_json()
        else:
            super().do_GET()

    def _serve_files_json(self):
        root = os.path.dirname(os.path.abspath(__file__))
        files = sorted(
            f for f in os.listdir(root)
            if f.lower().endswith('.csv') or f.lower().endswith('.xlsx')
        )
        body = json.dumps(files).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # suppress per-request log noise


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with http.server.HTTPServer(('', PORT), FilesAPIHandler) as httpd:
        # Run the server in a daemon thread.
        # serve_forever() blocks on select() internally, which does not reliably
        # receive Ctrl-C (SIGINT) on Windows.  Sleeping in the main thread does,
        # so Ctrl-C is caught here and we call shutdown() to stop the server thread.
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()

        print(f'Serving at http://localhost:{PORT}/')
        print('Press Ctrl+C to stop.')

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\nStopping...')
            httpd.shutdown()

    print('Server stopped.')
    sys.exit(0)


if __name__ == '__main__':
    main()
