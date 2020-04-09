import http.server
import socketserver

PORT = 8080

if __name__ == "__main__":
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as http_daemon:
        print("serving at port", PORT)
        http_daemon.serve_forever()
