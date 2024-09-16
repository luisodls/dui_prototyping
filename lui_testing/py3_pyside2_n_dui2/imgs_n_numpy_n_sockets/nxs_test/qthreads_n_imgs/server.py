import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import time, subprocess

from dxtbx.model.experiment_list import ExperimentListFactory
from dxtbx.flumpy import to_numpy


def get_experiments(experiment_path):
    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentListFactory.from_json_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments

def image_loading(img_num):
    experiments = get_experiments("imported.expt")
    my_sweep = experiments.imagesets()[0]
    raw_dat = my_sweep.get_raw_data(img_num)
    data_xy_flex = raw_dat[0].as_double()
    np_arr2 = to_numpy(data_xy_flex)
    txt_slice = str(np_arr2[50:90,40:80])
    return txt_slice


class ReqHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes('Test #6.5 ... multitasking & GUI \n', 'utf-8'))

        url_path = self.path
        dict_cmd = parse_qs(urlparse(url_path).query)
        print("dict_cmd =", dict_cmd)
        num_of_imgs = int(dict_cmd['num_of_imgs'][0])

        str_2_send = 'num_of_imgs =' + str(num_of_imgs)
        print(str_2_send)

        for img_num in range(num_of_imgs):
            img_slice = image_loading(img_num)
            str_n_X = img_slice + ' \n'
            self.wfile.write(bytes(str_n_X, 'utf-8'))

        print("sending /*EOF*/")
        self.wfile.write(bytes('/*EOF*/', 'utf-8'))


if __name__ == "__main__":
    PORT = 8080
    with socketserver.ThreadingTCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

