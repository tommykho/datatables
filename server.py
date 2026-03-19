"""
Simple HTTP server for the datatables viewer.
Serves the current directory at http://localhost:8000/
Press Ctrl+C to stop gracefully.
"""
import http.server
import sys

PORT = 8000


def main():
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda self, fmt, *args: None   # suppress per-request logs

    with http.server.HTTPServer(('', PORT), handler) as httpd:
        print(f'Serving at http://localhost:{PORT}/')
        print('Press Ctrl+C to stop.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
            sys.exit(0)


if __name__ == '__main__':
    main()
