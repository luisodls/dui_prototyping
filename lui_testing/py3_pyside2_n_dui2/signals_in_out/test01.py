import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools


class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.num = 0

        #Next line is NOT doing what I wanted, to return data with connect
        self.data_test = self.window.Button1.clicked.connect(self.clicked)

        self.window.PrintDataButton.clicked.connect(self.imprime)
        self.window.show()

    def clicked(self):
        print("clicked")
        self.num += 1
        print("self.num =", self.num)
        return int(self.num)

    def imprime(self):
        print("self.data_test =", self.data_test)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

