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
        self.wfile.write(bytes('<html><head><title>Python test server</title>', 'utf-8'))
        self.wfile.write(bytes('    </head>                                  ', 'utf-8'))
        self.wfile.write(bytes('    <body>                                   ', 'utf-8'))
        self.wfile.write(bytes('        <h1>Test 02</h1>                     ', 'utf-8'))
        self.wfile.write(bytes('        <p>Hi from the HTTP Server #2 </p>   ', 'utf-8'))
        self.wfile.write(bytes('    </body>                                  ', 'utf-8'))
        self.wfile.write(bytes('</html>                                      ', 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

