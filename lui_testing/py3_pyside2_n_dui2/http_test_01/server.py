import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as http_server:
    print("serving at port", PORT)
    http_server.serve_forever()
