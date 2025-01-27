from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        ''' Sets headers required for CORS '''
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def do_GET(self):
        # Set response status code and headers
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Send a JSON response
        response = {"message": "Hello from the Python server!"}
        self.wfile.write(json.dumps(response).encode("utf-8"))

# Start the server
def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
