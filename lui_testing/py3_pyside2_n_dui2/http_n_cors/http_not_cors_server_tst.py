#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps

""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

  def send_ok_dict(self):
      '''used by both, GET or POST,'''
      response = {}
      response["status"] = "OK"
      self.wfile.write(bytes(dumps(response), "utf8"))

  def do_GET(self):
      print("do_GET")
      self.send_response(200)
      self.end_headers()
      self.send_ok_dict()

  def do_POST(self):
      print("do_POST")
      self.send_response(200)
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
