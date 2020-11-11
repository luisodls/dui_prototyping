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
        self.window.GrayButton.clicked.connect(self.gray_but)
        self.window.pushButton.clicked.connect(self.but_clic)
        self.enable_state = True
        self.window.show()

    def gray_but(self):
        print("GrayButton clicked")
        self.enable_state = not self.enable_state
        self.window.pushButton.setEnabled(self.enable_state)

    def but_clic(self):
        print("pushButton clicked")



if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()
    sys.exit(app.exec_())
