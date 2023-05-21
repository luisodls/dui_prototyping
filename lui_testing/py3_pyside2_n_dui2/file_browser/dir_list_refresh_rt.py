
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import os, sys

class MyDirView_list(QListWidget):
    def __init__(self, parent = None):
        super(MyDirView_list, self).__init__(parent)
        self.itemClicked.connect(self.someting_click)
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)

    def enter_list(self, lst_in):
        self.items_list = []
        for single_file in lst_in:
            tst_item = QListWidgetItem(single_file["name"])
            tst_item.setIcon(QIcon("../icon_tst/icon_resources/import.png"))
            tst_item.tst_num = single_file["numb"]
            self.items_list.append(tst_item)

        self.draw_items()

    def draw_items(self):
        self.clear()
        for tst_item in self.items_list:
            self.addItem(tst_item)

    def someting_click(self, item):
        print("tst_num =", item.tst_num)


class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "simple.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI Cloud")

        self.lst_vw =  MyDirView_list()
        self.lst_dir = []

        for nm in range(30):
            self.lst_dir.append(
                {
                    "name":   "a" * nm,
                    "numb":     50 - nm
                }
            )
        self.lst_vw.enter_list(self.lst_dir)

        self.window.horiz_2_views_Layout.addWidget(self.lst_vw)
        self.window.RefreshButton.clicked.connect(self.Refresh_butt_clic)
        self.window.show()

    def Refresh_butt_clic(self):
        print("Refresh_butt_clic")
        self.lst_vw.draw_items()

if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()

    sys.exit(app.exec_())
