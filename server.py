"""
Simple HTTP server for the datatables viewer.
Serves the current directory at http://localhost:8000/

Key difference from plain `python -m http.server`:
  Always returns a real directory listing for folder requests instead of
  silently falling back to index.html. This lets the browser-side folder
  scan (fetch('./')) find .csv and .xlsx files reliably.

Press Ctrl+C to stop gracefully.
"""
import http.server
import os
import sys

PORT = 8000


class DirectoryListingHandler(http.server.SimpleHTTPRequestHandler):
    """Like SimpleHTTPRequestHandler but never auto-serves index.html for directories.

    python -m http.server normally returns index.html when it exists in a
    directory. That breaks the client-side fetch('./') folder scan because the
    response is the app HTML, not a listing with .csv/.xlsx hrefs.
    Overriding send_head() so directory paths always trigger list_directory().
    """

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            # Redirect if the trailing slash is missing (same as base class)
            if not self.path.endswith('/'):
                self.send_response(301)
                self.send_header('Location', self.path + '/')
                self.end_headers()
                return None
            # Always return the real directory listing, never index.html
            return self.list_directory(path)
        return super().send_head()

    # Suppress per-request log noise; remove this method to re-enable logging.
    def log_message(self, fmt, *args):
        pass


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with http.server.HTTPServer(('', PORT), DirectoryListingHandler) as httpd:
        print(f'Serving at http://localhost:{PORT}/')
        print('Press Ctrl+C to stop.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
            sys.exit(0)


if __name__ == '__main__':
    main()
