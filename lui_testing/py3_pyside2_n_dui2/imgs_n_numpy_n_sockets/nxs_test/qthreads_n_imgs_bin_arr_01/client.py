from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork
import sys, time
import requests
import numpy as np


class Run_n_Output(QtCore.QThread):
    line_out = QtCore.Signal(str)
    def __init__(self, request):
        super(Run_n_Output, self).__init__()
        self.request = request

    def run(self):


        cont_leng = self.request.headers.get('content-length', 0)

        print('content-length =', cont_leng)

        cont_data = self.request.content
        np_slice = from_bin_2_np_arr(cont_data)
        self.line_out.emit(str(np_slice))

def from_bin_2_np_arr(byte_json):
    try:
        print("type(byte_json) =", type(byte_json))
        print("len(byte_json) = ", len(byte_json))
        d1d2_n_arr1d = np.frombuffer(byte_json, dtype = float)
        d1 = int(d1d2_n_arr1d[0])
        d2 = int(d1d2_n_arr1d[1])
        np_array_out = d1d2_n_arr1d[2:].reshape(d1, d2)

    except TypeError:
        print("TypeError(from_bin_2_np_arr)")
        np_array_out = None

        tmp_off = '''
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

    def add_line(self, new_line):
        print("new_line =", new_line)

    def run_ended(self):
        print("run_ended")

    def request_launch(self):
        cmd = {'img_num': self.img_num}
        req_get = requests.get('http://localhost:8080/', stream = True, params = cmd)

        self.thrd = Run_n_Output(req_get)
        self.thrd.line_out.connect(self.add_line)
        self.thrd.finished.connect(self.run_ended)
        self.thrd.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())



