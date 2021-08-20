import requests, json, os, sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

def iter_gui(myself, currentItem):
    for child in myself["list_child"]:
        if myself["isdir"]:
            dirItem = QTreeWidgetItem(currentItem)
            dirItem.setText(0, child["file_name"])
            iter_gui(child, dirItem)

        else:
            fileItem = QTreeWidgetItem(currentItem)
            fileItem.setText(0, child["file_name"])


class MyTree(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTree, self).__init__(parent=parent)
        self.show()

    def fillTree(self, lst_dic):
        iter_gui(lst_dic, self)


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.t_view = MyTree()
        mainLayout.addWidget(self.t_view)
        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.json_data_request)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)

    def json_data_request(self):
        req_get = requests.get(
            'http://localhost:8080/', stream = True,
            params = {"path":"/scratch/dui_tst/"}, timeout = 3
        )
        str_lst = ''
        line_str = ''
        times_loop = 10
        json_out = ""
        for count_times in range(times_loop):
            tmp_dat = req_get.raw.readline()
            line_str = str(tmp_dat.decode('utf-8'))
            if line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

            else:
                str_lst = line_str

            if count_times == times_loop - 1:
                print('to many "lines" in http response')
                json_out = None

        if json_out is not None:
            json_out = json.loads(str_lst)
            #print("json_out =", json_out)

            self.t_view.fillTree(json_out)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
