import http.server
import socketserver

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
        old_stable = '''
        self.wfile.write(bytes('<html><body><p>', 'utf-8'))
        self.wfile.write(bytes('Hi from the HTTP Server #3 ', 'utf-8'))
        self.wfile.write(bytes('</p></body></html>', 'utf-8'))
        '''

        self.wfile.write(bytes('                                ', 'utf-8'))
        self.wfile.write(bytes(' *** TEST 03 ***                ', 'utf-8'))
        self.wfile.write(bytes('                                ', 'utf-8'))
        self.wfile.write(bytes('     YEY                        ', 'utf-8'))
        self.wfile.write(bytes('                                ', 'utf-8'))


        print("dir(self)", dir(self))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

