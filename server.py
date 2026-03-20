"""
Simple HTTP server for the datatables viewer.
Serves the current directory at http://localhost:8000/

Extra endpoint:
  GET /api/files  — returns a JSON array of all .csv and .xlsx filenames
                    in the served directory, sorted alphabetically.
                    Used by the browser-side folder scan in index.html.

Press Ctrl+C to stop gracefully.
"""
import http.server
import json
import os
import sys

PORT = 8000


class FilesAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Like SimpleHTTPRequestHandler but adds GET /api/files.

    The browser calls fetch('/api/files') to discover available CSV/XLSX files
    without any HTML-parsing hacks or directory-listing conflicts.
    All other requests (including GET /) are handled by the base class, so
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

    # Suppress per-request log noise; remove this method to re-enable logging.
    def log_message(self, fmt, *args):
        pass


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with http.server.HTTPServer(('', PORT), FilesAPIHandler) as httpd:
        print(f'Serving at http://localhost:{PORT}/')
        print('Press Ctrl+C to stop.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
            sys.exit(0)


if __name__ == '__main__':
    main()
