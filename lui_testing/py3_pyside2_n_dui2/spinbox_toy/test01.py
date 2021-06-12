import sys, time
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class my_new_spin(QSpinBox):
    def __init__(self, parent = None):
        super(my_new_spin, self).__init__(parent)
        print("my_new_spin.__init__")
        print("dir(my_new_spin)", dir(self))

        '''
    def mouseReleaseEvent(self, event):
        print("my_new_spin(mouseReleaseEvent)")

    def changeEvent(self, event):
        print("my_new_spin(changeEvent)")

    def mousePressEvent(self, event):
        print("my_new_spin(mousePressEvent)")
        '''

    def wheelEvent(self, event):
        print("my_new_spin(wheelEvent)")


class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        custom_spin = my_new_spin()
        self.window.SpinHorizontalLayout.addWidget(custom_spin)
        custom_spin.valueChanged.connect(self.custom_spin_val_new)

        self.window.MySpinBox.valueChanged.connect(self.val_new)
        self.window.show()

    def val_new(self, new_val):
        time.sleep(1)
        print("MySpinBox(new_val):", new_val)

    def custom_spin_val_new(self, new_val):
        time.sleep(1)
        print("custom_spin(new_val):", new_val)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

