#import http.server
from urllib.parse import urlparse, parse_qs
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


#class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
class ThreadingTCPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        url_path = self.path
        print('urlparse(self.path).query', parse_qs(urlparse(url_path).query))

        self.wfile.write(bytes('Test #4\n', 'utf-8'))
        self.wfile.write(bytes('1234567890\n', 'utf-8'))
        self.wfile.write(bytes('12345678901234567890\n', 'utf-8'))
        self.wfile.write(bytes('123456789012345678901234567890\n', 'utf-8'))

        print("starting to send numbers ...")
        for num in range(9):
            num_str = ' num = ' + str(num) + '\n'
            time.sleep(0.5)
            print("sending <<", num_str, ">> str ")
            self.wfile.write(bytes(num_str, 'utf-8'))

        print("... finished sending numbers")
        print("sending /*EOF*/")
        self.wfile.write(bytes('/*EOF*/', 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    #httpd = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    httpd = HTTPServer(("", PORT), ThreadingTCPServer)
    httpd.socket = ssl.wrap_socket (
        httpd.socket, keyfile = "testeando.key",
        certfile = "testeando.pem", server_side = True
    )

    print("serving at port", PORT, "with:ThreadingTCPServer")
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n Keyboard-Interrupt received")
        httpd.server_close()

