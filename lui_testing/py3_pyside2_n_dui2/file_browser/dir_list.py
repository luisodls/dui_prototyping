
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import os, sys

class MyDirView(QListWidget):
    def __init__(self, parent = None):
        super(MyDirView, self).__init__(parent)
        self.itemClicked.connect(self.someting_click)

    def add_dummy_item(self, str_in, num):
        tst_item = QListWidgetItem(str_in)
        tst_item.setIcon(QIcon("../icon_tst/icon_resources/import.png"))
        tst_item.tst_num = 50 - num
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

        self.lst_vw =  MyDirView()
        for nm in range(10):
            self.lst_vw.add_dummy_item("a" * nm, nm)

        self.window.verticalLayout.addWidget(self.lst_vw)
        self.window.show()


if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()

    sys.exit(app.exec_())
