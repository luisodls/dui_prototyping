from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork
import sys, time, zlib
import requests
import numpy as np

class Run_n_Output(QtCore.QThread):
    array_out = QtCore.Signal(str)
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
            print("progress =", progress)

        unzip_data = zlib.decompress(compresed)
        print("get_request_real_time ... downloaded")
        end_data = from_bin_2_np_arr(unzip_data)
        self.array_out.emit(str(end_data))



def from_bin_2_np_arr(byte_json):
    code_removed_for_testing = '''
    try:
    '''
    print("len(byte_json) = ", len(byte_json))
    d1d2_n_arr1d = np.frombuffer(byte_json, dtype = float)
    d1 = int(d1d2_n_arr1d[0])
    d2 = int(d1d2_n_arr1d[1])
    np_array_out = d1d2_n_arr1d[2:].reshape(d1, d2)

    code_removed_for_testing = '''
    except TypeError:
        print("TypeError(from_bin_2_np_arr)")
        np_array_out = None

    except ValueError:
        print("ValueError(from_bin_2_np_arr)")
        np_array_out = None
    '''

    return np_array_out


class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        send2serverButton = QtWidgets.QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        self.img_num = 5
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(QtWidgets.QLabel(
            " \n ready  to ask for  image number " + str(self.img_num) + "\n"
        ))
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test with HTTP")

    def add_array(self, new_array):
        print("new array =\n", new_array)

    def run_ended(self):
        print("run_ended")

    def request_launch(self):
        cmd = {'img_num': self.img_num}
        req_get = requests.get(
            'http://localhost:8080/', stream = True, params = cmd
        )
        self.thrd = Run_n_Output(req_get)
        self.thrd.array_out.connect(self.add_array)
        self.thrd.finished.connect(self.run_ended)
        self.thrd.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())



