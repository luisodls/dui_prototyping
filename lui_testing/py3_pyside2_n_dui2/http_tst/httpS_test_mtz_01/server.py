import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import time, subprocess, json
from json import dumps

class ReqHandler(http.server.BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        ''' Sets headers required for CORS '''
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers", "x-api-key,Content-Type"
        )

    def send_ok_dict(self):
        '''used by both, GET or POST,'''
        response = {}
        response["status"] = "OK"
        self.wfile.write(bytes(dumps(response), "utf8"))

    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        #self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print("post_body =", post_body)
        self.send_ok_dict()


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

