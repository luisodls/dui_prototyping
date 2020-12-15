import http.server
import socketserver

class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        f = open("page.html", "r")
        str_lst = f.readlines()
        f.close()

        for lin in str_lst:
            self.wfile.write(bytes(lin, 'utf-8'))

        for lin in str_lst:
            self.wfile.write(bytes("/*EOF*/", 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

