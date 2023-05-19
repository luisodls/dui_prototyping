
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import os, sys

class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "simple.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI Cloud")

        self.lst_vw =  QListWidget()
        self.window.verticalLayout.addWidget(self.lst_vw)

        self.lst_vw.itemClicked.connect(self.someting_click)
        self.window.show()

    def someting_click(self, item):
        print("\n item =", item)
        print("tst_num =", item.tst_num)

    def add_something_dummy(self, str_in, num):
        tst_item = QListWidgetItem(str_in)
        tst_item.setIcon(QIcon("../icon_tst/icon_resources/import.png"))
        tst_item.tst_num = 50 - num
        self.lst_vw.addItem(tst_item)



if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()

    for nm in range(10):
        m_obj.add_something_dummy("a" * nm, nm)

    sys.exit(app.exec_())
