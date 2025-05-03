from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is alive!')

def run_server():
    port = int(os.environ.get('PORT', 3000))  # Use $PORT from env or default to 3000
    server_address = ('0.0.0.0', port)        # Bind to all interfaces
    httpd = HTTPServer(server_address, KeepAliveHandler)
    print(f"Keep-alive server running on port {port}")
    httpd.serve_forever()

def keep_alive():
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
