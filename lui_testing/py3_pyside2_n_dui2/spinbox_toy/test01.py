import sys, time
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class Form(QObject):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")
        self.window.MySpinBox.valueChanged.connect(self.val_new)
        self.window.show()

    def val_new(self, new_val):
        time.sleep(1)
        print("MySpinBox(new_val):", new_val)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

