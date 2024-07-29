#from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *




import sys, time, zlib, time
import requests
import numpy as np


class np2bmp_monocrome(object):
    def __init__(self):
        self.all_chan_byte = np.empty( (255), 'int')
        for i in range(255):
            self.all_chan_byte[i] = i

    def img_2d_rgb(
        self, data2d = None, invert = False, i_min_max = [None, None]
    ):
        data2d_ini = np.copy(data2d)
        if(i_min_max == [None, None]):
            i_min_max = [data2d_ini.min(), data2d_ini.max()]
            print("no max and min provided, assuming:", i_min_max)

        elif(i_min_max[0] > data2d_ini.min() or i_min_max[1] < data2d_ini.max()):
            print("clipping to [max, min]:", i_min_max, "  ...")
            np.clip(data2d_ini, i_min_max[0], i_min_max[1], out = data2d_ini)
            print("... done clipping")

        self.width = np.size( data2d_ini[0:1, :] )
        self.height = np.size( data2d_ini[:, 0:1] )

        data2d_pos = data2d_ini[:,:] - i_min_max[0] + 1.0
        data2d_pos_max = data2d_pos.max()

        calc_pos_max = i_min_max[1] - i_min_max[0] + 1.0
        if(calc_pos_max > data2d_pos_max):
            data2d_pos_max = calc_pos_max

        div_scale = 254.0 / data2d_pos_max
        data2d_scale = np.multiply(data2d_pos, div_scale)
        if(invert == True):
            for x in np.nditer(
                data2d_scale[:,:], op_flags=['readwrite'],
                flags=['external_loop']
            ):
                x[...] = 254.0 - x[...]

        img_array = np.zeros([self.height, self.width, 4], dtype=np.uint8)
        img_all_chanl = np.empty( (self.height, self.width), 'int')
        scaled_i = np.empty( (self.height, self.width), 'int')
        scaled_i[:,:] = data2d_scale[:,:]

        img_all_chanl[:,:] = scaled_i[:,:]
        for x in np.nditer(
            img_all_chanl[:,:], op_flags=['readwrite'],
            flags=['external_loop']
        ):
            x[...] = self.all_chan_byte[x]

        img_array[:, :, 3] = 255
        img_array[:, :, 2] = img_all_chanl[:,:] #Blue
        img_array[:, :, 1] = img_all_chanl[:,:] #Green
        img_array[:, :, 0] = img_all_chanl[:,:] #Red
        return img_array



def from_bin_2_np_arr(byte_json):
    print("len(byte_json) = ", len(byte_json))
    d1d2_n_arr1d = np.frombuffer(byte_json, dtype = float)
    d1 = int(d1d2_n_arr1d[0])
    d2 = int(d1d2_n_arr1d[1])
    np_array_out = d1d2_n_arr1d[2:].reshape(d1, d2)
    return np_array_out


class Run_n_Output(QThread):
    array_out = Signal(list)
    progress_out = Signal(int)
    def __init__(self, request):
        super(Run_n_Output, self).__init__()
        self.request = request

    def run(self):
        req_head = self.request.headers.get('content-length', 0)
        total_size = int(req_head) + 1
        print("total_size =" + str(total_size))
        block_size = int(total_size / 6 * 1024)
        max_size = 16384
        if block_size > max_size:
            block_size = max_size

        print("block_size =" + str(block_size))

        downloaded_size = 0
        compresed = bytes()
        for data in self.request.iter_content(block_size):
            compresed += data
            downloaded_size += block_size
            progress = int(100.0 * (downloaded_size / total_size))
            self.progress_out.emit(progress)

        unzip_data = zlib.decompress(compresed)
        print("get_request_real_time ... downloaded")
        end_data = from_bin_2_np_arr(unzip_data)
        self.array_out.emit([end_data, total_size])


class Client( QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        send2serverButton =  QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        self.img_label =  QLabel("\n\n click button \n\n")
        self.prog_label =  QLabel("\n progress = ? \n")
        mainLayout =  QVBoxLayout()
        mainLayout.addWidget(self.img_label)
        mainLayout.addWidget(self.prog_label)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test with HTTP")

        self.bmp_m_cro = np2bmp_monocrome()


    def new_progress(self, progress):
        self.prog_label.setText("\n progress = " + str(progress) + " \n")

    def add_array(self, lst_w_arr):
        new_array = lst_w_arr[0]
        rgb_np = self.bmp_m_cro.img_2d_rgb(
            data2d = new_array, invert = False, i_min_max = [-2, 10]
        )
        q_img = QImage(
            rgb_np.data,
            np.size(rgb_np[0:1, :, 0:1]),
            np.size(rgb_np[:, 0:1, 0:1]),
            QImage.Format_ARGB32
        )
        tmp_pixmap = QPixmap.fromImage(q_img)
        self.img_label.setPixmap(tmp_pixmap)


    def run_ended(self):
        self.prog_label.setText("\n progress = ? \n")
        print("run_ended")

    def request_launch(self):
        self.sycle_img_num = 1
        timer = QTimer(self)
        timer.timeout.connect(self.refresh_img_loop)
        timer.start(100)

    def refresh_img_loop(self):
        self.sycle_img_num += 1
        print("updating image # ", self.sycle_img_num)
        cmd = {'img_num': self.sycle_img_num}
        req_get = requests.get(
            'http://localhost:8080/', stream = True, params = cmd
        )
        self.thrd = Run_n_Output(req_get)
        self.thrd.array_out.connect(self.add_array)
        self.thrd.finished.connect(self.run_ended)
        self.thrd.progress_out.connect(self.new_progress)
        self.thrd.start()


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())



