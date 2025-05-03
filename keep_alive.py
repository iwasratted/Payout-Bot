from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is alive!')

def run_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, KeepAliveHandler)
    print("Keep-alive server running on port 3000")
    httpd.serve_forever()

def keep_alive():
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
