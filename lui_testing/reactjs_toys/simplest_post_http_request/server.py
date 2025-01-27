from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Set headers to enable CORS."""
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle preflight requests."""
        self.send_response(204)  # No Content
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        """Handle POST requests."""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # Read and process the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Received POST data: {post_data}")

        # Send a JSON response
        response = {"message": "Data received successfully!", "received_data": post_data}
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Start the server
def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
