import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import time, subprocess

class ReqHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes('Test #6.5 ... multitasking & GUI \n', 'utf-8'))

        url_path = self.path
        dict_cmd = parse_qs(urlparse(url_path).query)
        print("dict_cmd =", dict_cmd)
        cmd_str = dict_cmd['command'][0]

        str_2_send = 'cmd_in =' + cmd_str + ' \n'
        print(str_2_send)
        self.wfile.write(bytes(str_2_send, 'utf-8'))

        print("sending /*EOF*/")
        self.wfile.write(bytes('/*EOF*/', 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.ThreadingTCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

