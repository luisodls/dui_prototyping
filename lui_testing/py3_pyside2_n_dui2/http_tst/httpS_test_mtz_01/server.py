import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import time, subprocess, json
from json import dumps

class ReqHandler(http.server.BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        ''' Sets headers required for CORS '''
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers", "x-api-key,Content-Type"
        )

    def send_ok_dict(self):
        '''used by both, GET or POST,'''
        response = {}
        response["status"] = "OK"
        self.wfile.write(bytes(dumps(response), "utf8"))

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes('Test #5\n', 'utf-8'))

        url_path = self.path
        dict_cmd = parse_qs(urlparse(url_path).query)
        cmd_str = dict_cmd['command'][0]
        cmd_lst = cmd_str.split(' ')

        print("\n Running:", cmd_lst, "\n")
        proc = subprocess.Popen(
            cmd_lst,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        line = None
        while proc.poll() is None or line != '':
            line = proc.stdout.readline()[:-1]
            print("StdOut>> ", line)
            self.wfile.write(bytes(line + '\n', 'utf-8'))

        proc.stdout.close()
        print("sending /*EOF*/")
        self.wfile.write(bytes('/*EOF*/', 'utf-8'))
        #self.send_ok_dict()


    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        #self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)

        print("post_body =", post_body)

        '''
        body_str = str(post_body.decode('utf-8'))
        url_dict = json.loads(body_str)
        msg = url_dict['message']
        print("msg =", msg)
        if msg != "":
            uni_controler.run(msg)
            print("-----------------------------------------------")
            show_tree(uni_controler)
            self.send_ok_dict(msg)

        else:
            self.send_ok_dict()
        '''
        self.send_ok_dict()



if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

