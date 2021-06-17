import http.server
import socketserver

import time

class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self, str_in = None):
        print("str_in =", str_in)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes('                                \n', 'utf-8'))
        self.wfile.write(bytes(' *** TEST 03 ***                \n', 'utf-8'))
        self.wfile.write(bytes('                                \n', 'utf-8'))
        self.wfile.write(bytes('     YEY                        \n', 'utf-8'))
        self.wfile.write(bytes('                                \n', 'utf-8'))

        print("starting to send numbers ...")
        for num in range(3):
            num_str = ' num = ' + str(num) + '\n'
            time.sleep(5.5)
            print("sending <<", num_str, ">> str ")
            self.wfile.write(bytes(num_str, 'utf-8'))

        print("... finished sending numbers")
        print("sending /*EOF*/")
        self.wfile.write(bytes('/*EOF*/', 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

