import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

str_2_print = "http://localhost:" + str(PORT) + "/"

with socketserver.TCPServer(("", PORT), Handler) as http_daemon:
    print("serving at URL:", str_2_print)
    http_daemon.serve_forever()
