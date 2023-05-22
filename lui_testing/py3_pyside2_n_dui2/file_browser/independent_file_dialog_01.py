import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import random

def sort_dict_list(lst_in):
    list_size = len(lst_in)
    for i in range(list_size):
        min_index = i
        for j in range(i + 1, list_size):
            if lst_in[min_index]["name"] > lst_in[j]["name"]:
                min_index = j

        lst_in[i], lst_in[min_index] = lst_in[min_index], lst_in[i]

    return lst_in


class MyDirView_list(QListWidget):
    def __init__(self, parent = None):
        super(MyDirView_list, self).__init__(parent)
        self.itemClicked.connect(self.someting_click)
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)

    def enter_list(self, lst_in):
        lst_in = sort_dict_list(lst_in)

        DirPixMapi = getattr(QStyle, 'SP_DirIcon')
        FilePixMapi = getattr(QStyle, 'SP_FileIcon')
        icon_dict = {
            "Dir":self.style().standardIcon(DirPixMapi),
            "File":self.style().standardIcon(FilePixMapi)
        }
        self.items_list = []
        for single_file in lst_in:
            tst_item = QListWidgetItem(single_file["name"])
            tst_item.isdir = single_file["isdir"]
            if tst_item.isdir:
                tst_item.setIcon(icon_dict["Dir"])

            else:
                tst_item.setIcon(icon_dict["File"])

            self.items_list.append(tst_item)

        self.clear()
        for tst_item in self.items_list:
            self.addItem(tst_item)

    def someting_click(self, item):
        print("isdir =", item.isdir)


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()

        self.lst_vw =  MyDirView_list()
        self.build_content()
        mainLayout.addWidget(self.lst_vw)

        OpenButton = QPushButton(" Open ")
        OpenButton.clicked.connect(self.open_file)
        mainLayout.addWidget(OpenButton)

        CancelButton = QPushButton(" Cancel ")
        CancelButton.clicked.connect(self.cancel_opp)
        mainLayout.addWidget(CancelButton)

        self.setLayout(mainLayout)

    def build_content(self):
        os_listdir = os.listdir("/")
        lst_dir = []
        for nm, f_name in enumerate(os_listdir):
            f_isdir = os.path.isdir("/" + f_name)
            lst_dir.append(
                {
                    "name":   f_name, "isdir":  f_isdir
                }
            )

        self.lst_vw.enter_list(lst_dir)

    def open_file(self):
        print("Launch open_file ")
        self.build_content()

    def cancel_opp(self):
        print("Cancel clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
