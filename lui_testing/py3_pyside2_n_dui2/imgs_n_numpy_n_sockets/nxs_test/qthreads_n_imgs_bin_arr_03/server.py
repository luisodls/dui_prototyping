import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import time, subprocess, zlib
import numpy as np

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
    np_arr = to_numpy(data_xy_flex)
    slice_out = np_arr[50:590,40:680]
    return slice_out


def np_arr_2_byte_stream(np_arr_in):
    d1 = np_arr_in.shape[0]
    d2 = np_arr_in.shape[1]
    img_arr = np.zeros(d1 * d2 + 2, dtype = float)
    img_arr[0] = float(d1)
    img_arr[1] = float(d2)
    img_arr[2:] = np_arr_in.ravel()
    byte_info = img_arr.tobytes(order='C')
    return byte_info


class ReqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = self.path
        dict_cmd = parse_qs(urlparse(url_path).query)
        print("dict_cmd =", dict_cmd)
        img_num = int(dict_cmd['img_num'][0])

        str_2_send = 'img_num =' + str(img_num)
        print(str_2_send)

        img_slice = image_loading(img_num)
        slice_bin = np_arr_2_byte_stream(img_slice)

        byt_data = zlib.compress(slice_bin)
        siz_dat = str(len(byt_data))
        print("\n siz_dat =", siz_dat)
        self.send_response(200)
        self.send_header('Content-type', 'application/zlib')
        self.send_header('Content-Length', siz_dat)
        self.end_headers()
        self.wfile.write(byt_data)


if __name__ == "__main__":
    PORT = 8080
    with socketserver.ThreadingTCPServer(("", PORT), ReqHandler) as http_daemon:
        print("serving at port", PORT)
        try:
            http_daemon.serve_forever()

        except KeyboardInterrupt:
            http_daemon.server_close()

