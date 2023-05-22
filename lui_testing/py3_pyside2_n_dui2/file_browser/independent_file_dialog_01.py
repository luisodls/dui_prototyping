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

    file_clickled = Signal(dict)
    def __init__(self, parent = None):
        super(MyDirView_list, self).__init__(parent)
        self.itemClicked.connect(self.someting_click)
        self.itemDoubleClicked.connect(self.someting_2_clicks)
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
            tst_item.f_isdir = single_file["isdir"]
            tst_item.f_path = str(single_file["path"])
            if tst_item.f_isdir:
                tst_item.setIcon(icon_dict["Dir"])

            else:
                tst_item.setIcon(icon_dict["File"])

            self.items_list.append(tst_item)

        self.clear()
        for tst_item in self.items_list:
            self.addItem(tst_item)

    def someting_click(self, item):
        self.file_clickled.emit(
            {"isdir":item.f_isdir, "path":item.f_path}
        )

    def someting_2_clicks(self, item):
        self.file_clickled.emit(
            {"isdir":item.f_isdir, "path":item.f_path}
        )

##############################################################################
class PathButtons(QWidget):
    def __init__(self, parent = None):
        super(PathButtons, self).__init__()
        main_h_lay = QHBoxLayout()

        for tst_time in range(9):
            new_butt = QPushButton(str(tst_time) * tst_time)
            main_h_lay.addWidget(new_butt)

        self.setLayout(main_h_lay)



class PathBar(QWidget):
    def __init__(self, parent = None):
        super(PathBar, self).__init__(parent)
        mainLayout = QVBoxLayout()
        path_buttons = PathButtons(self)
        scroll_path = QScrollArea()
        scroll_path.setWidget(path_buttons)
        mainLayout.addWidget(scroll_path)
        self.setLayout(mainLayout)

        self.bt_size = self.height()
        print("self.bt_size", self.bt_size)
        self.setFixedHeight(self.bt_size * 3)


##############################################################################
class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()

        path_bar = PathBar(self)
        mainLayout.addWidget(path_bar)

        self.current_file = None
        self.lst_vw =  MyDirView_list()
        self.build_content(os.sep)
        self.lst_vw.file_clickled.connect(self.fill_clik)
        mainLayout.addWidget(self.lst_vw)

        OpenButton = QPushButton(" Open ")
        OpenButton.clicked.connect(self.open_file)
        mainLayout.addWidget(OpenButton)

        CancelButton = QPushButton(" Cancel ")
        CancelButton.clicked.connect(self.cancel_opp)
        mainLayout.addWidget(CancelButton)

        self.setLayout(mainLayout)

    def build_content(self, ini_path):
        parents_list = ini_path.split(os.sep)[1:-1]
        print("parents_list =", parents_list)

        os_listdir = os.listdir(ini_path)
        lst_dir = []
        for nm, f_name in enumerate(os_listdir):
            f_path = ini_path + f_name
            f_isdir = os.path.isdir(f_path)
            lst_dir.append(
                {
                    "name": f_name, "isdir":  f_isdir, "path": f_path
                }
            )

        self.lst_vw.enter_list(lst_dir)

    def fill_clik(self, fl_dic):
        print("isdir = ", fl_dic["isdir"])
        print("path = ", fl_dic["path"])
        if fl_dic == self.current_file and self.current_file["isdir"]:
            self.build_content(self.current_file["path"] + os.sep)

        self.current_file = fl_dic

    def open_file(self):
        try:
            if self.current_file["isdir"]:
                self.build_content(self.current_file["path"] + os.sep)

            else:
                print("Opened: ", self.current_file["path"])

        except TypeError:
            print("no file selected yet")

    def cancel_opp(self):
        print("Cancel clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
