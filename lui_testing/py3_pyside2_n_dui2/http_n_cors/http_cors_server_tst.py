#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps

""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

  def _send_cors_headers(self):
      ''' Sets headers required for CORS '''
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

  def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

  def send_ok_dict(self):
      '''used by both, GET or POST,'''
      response = {}
      response["status"] = "OK"
      self.wfile.write(bytes(dumps(response), "utf8"))

  def do_GET(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()
      self.send_ok_dict()

  def do_POST(self):
      self.send_response(200)
      self._send_cors_headers()
      self.send_header("Content-Type", "application/json")
      self.end_headers()

      dataLength = int(self.headers["Content-Length"])
      print("dataLength =", dataLength)
      data = self.rfile.read(dataLength)
      print("data =", data)
      self.send_ok_dict()



print("Starting server")

ip_adr = "127.0.0.1"
port_num = 45678
httpd = HTTPServer((ip_adr, port_num), RequestHandler)
full_url = "http://" + ip_adr + ":" + str(port_num)
print("Hosting server on:", full_url )
httpd.serve_forever()
