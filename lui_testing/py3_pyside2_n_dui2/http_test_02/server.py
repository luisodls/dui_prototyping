import http.server
import socketserver

class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        http_daemon.serve_forever()
