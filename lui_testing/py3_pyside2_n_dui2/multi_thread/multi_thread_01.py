import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class my_one(QThread):
    def __init__(self):
        super(my_one, self).__init__()

    def run(self):
        print("")


class MainImgViewObject(QObject):
    def __init__(self, parent = None):
        super(MainImgViewObject, self).__init__(parent)
        self.parent_app = parent
        self.window = QtUiTools.QUiLoader().load("main.ui")
        self.window.setWindowTitle("test")
        print("inside QObject")
        self.window.RunPushButton.clicked.connect(self.run_one_clicked)
        self.window.show()

    def run_one_clicked(self):
        print("run_one_clicked(MainImgViewObject)")


def main():
    app = QApplication(sys.argv)
    m_obj = MainImgViewObject(parent = app)
    print("before sys.exit")
    sys.exit(app.exec_())
    print("after sys.exit")


if __name__ == "__main__":
    main()

