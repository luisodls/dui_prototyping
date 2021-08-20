import http.server, socketserver
from urllib.parse import urlparse, parse_qs
import json, os

def iter_dict(file_path):
    file_name = file_path.split("/")[-1]
    local_dict = {
        "file_name": file_name, "file_path": file_path, "list_child": []
    }
    if os.path.isdir(file_path):
        local_dict["isdir"] = True
        for new_file_name in os.listdir(file_path):
            new_file_path = os.path.join(file_path, new_file_name)
            local_dict["list_child"].append(
                iter_dict(new_file_path)
            )

    else:
        local_dict["isdir"] = False

    return local_dict


class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        url_path = self.path
        url_dict = parse_qs(urlparse(url_path).query)
        print("url_dict =", url_dict)
        try:
            star_path = url_dict["path"][0]
            dic_lst_out = iter_dict(star_path)

            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            json_str = json.dumps(dic_lst_out) + '\n'
            self.wfile.write(bytes(json_str, 'utf-8'))

            print("sending /*EOF*/")
            self.wfile.write(bytes('/*EOF*/', 'utf-8'))

        except BrokenPipeError:
            print("\n *** BrokenPipeError *** while sending EOF or JSON \n")

        except ConnectionResetError:
            print("\n *** ConnectionResetError *** while sending EOF or JSON \n")


if __name__ == "__main__":
    PORT = 8080
    with socketserver.ThreadingTCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

