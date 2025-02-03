from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from old_tree_nav import runner, prin_lst, show_tree

""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        ''' Sets headers required for CORS '''
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def send_ok_dict(self, str_out = "Ok"):
        '''used by both, GET or POST,'''
        response = {}
        response["Answer"] = str_out
        self.wfile.write(json.dumps(response).encode('utf-8'))


    def do_GET(self):
        print("do_GET")
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        url_path = self.path
        url_dict = parse_qs(urlparse(url_path).query)

        print("url_path =", url_path)
        print("url_dict =", url_dict)

        #self.send_ok_dict(url_dict["msgHere"][0])

        lst_out = prin_lst(uni_controler.step_list, uni_controler.current)

        self.send_ok_dict(lst_out)
        #self.send_ok_dict(url_dict["msgHere"][0])


    def do_PUT(self):
        print("do_PUT")
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        print("dataLength =", dataLength)
        data = self.rfile.read(dataLength)
        print("data =", data)
        self.send_ok_dict()


    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body_str = str(post_body.decode('utf-8'))
        url_dict = json.loads(body_str)
        print("url_dict =", url_dict)
        msg = url_dict['message']
        print("msg =", msg)

        uni_controler.run(msg)
        prin_lst(uni_controler.step_list, uni_controler.current)
        print("-----------------------------------------------")
        show_tree(step = uni_controler.step_list[0], curr = uni_controler.current, indent = 1)

        self.send_ok_dict(msg)


if __name__ == "__main__":
    print("Starting server")

    uni_controler = runner()

    '''
    uni_controler = runner()

    command = ""
    while command.strip() != 'exit':
        # printing new list of steps
        #prin_lst(uni_controler.step_list, uni_controler.current)

        # showing showing tree
        print("________ showing steps tree:")
        show_tree(step = uni_controler.step_list[0], curr = uni_controler.current, indent = 1)

        try:
            command = str(input(">>> "))

        except:
            print("tweak key pressed ... quitting")
            sys.exit(0)

        uni_controler.run(command)

    '''


    ip_adr = "127.0.0.1"
    port_num = 45678
    httpd = HTTPServer((ip_adr, port_num), RequestHandler)
    full_url = "http://" + ip_adr + ":" + str(port_num)
    print("Hosting server on:", full_url )
    httpd.serve_forever()
