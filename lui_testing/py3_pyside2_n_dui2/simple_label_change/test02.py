import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple_02.ui")

        #self.in_label = QLabel("tmp ... text")

        self.PrintDataButton = QPushButton("txt tst", self.window)
        #self.PrintDataButton.setLabel(self.in_label)
        self.PrintDataButton.clicked.connect(self.imprime)
        self.window.show()

    def imprime(self):
        print("self.imprime")
        self.PrintDataButton.setText(" AAAAAAAAAAAa ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

