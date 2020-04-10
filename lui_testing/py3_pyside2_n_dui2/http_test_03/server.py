import http.server
import socketserver

import time

class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        '''

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes('                                \n', 'utf-8'))
        self.wfile.write(bytes(' *** TEST 03 ***                \n', 'utf-8'))
        self.wfile.write(bytes('                                \n', 'utf-8'))
        self.wfile.write(bytes('     YEY                        \n', 'utf-8'))
        self.wfile.write(bytes('                                \n', 'utf-8'))

        for num in range(10):
            num_str = str(num)
            print("num_str=", num_str)
            time.sleep(0.5)
            self.wfile.write(bytes(num_str, 'utf-8'))



if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

