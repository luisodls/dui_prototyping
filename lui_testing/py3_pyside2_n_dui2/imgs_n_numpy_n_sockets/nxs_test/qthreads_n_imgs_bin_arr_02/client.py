from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork
import sys, time, zlib, time
import requests
import numpy as np

def from_bin_2_np_arr(byte_json):
    print("len(byte_json) = ", len(byte_json))
    d1d2_n_arr1d = np.frombuffer(byte_json, dtype = float)
    d1 = int(d1d2_n_arr1d[0])
    d2 = int(d1d2_n_arr1d[1])
    np_array_out = d1d2_n_arr1d[2:].reshape(d1, d2)
    return np_array_out


class Run_n_Output(QtCore.QThread):
    array_out = QtCore.Signal(str)
    progress_out = QtCore.Signal(int)
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
        self.array_out.emit(str(end_data))


class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        send2serverButton = QtWidgets.QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        self.img_label = QtWidgets.QLabel("\n\n click button \n\n")
        self.prog_label = QtWidgets.QLabel("\n progress = ? \n")
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.img_label)
        mainLayout.addWidget(self.prog_label)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test with HTTP")

    def new_progress(self, progress):
        self.prog_label.setText("\n progress = " + str(progress) + " \n")

    def add_array(self, new_array):
        self.img_label.setText(new_array)

    def run_ended(self):
        self.prog_label.setText("\n progress = ? \n")
        print("run_ended")

    def request_launch(self):
        self.sycle_img_num = 1
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.refresh_img_loop)
        timer.start(200)

    def refresh_img_loop(self):
        self.sycle_img_num += 1
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
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())



