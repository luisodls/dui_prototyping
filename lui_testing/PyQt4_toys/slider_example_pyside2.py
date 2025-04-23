from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class Window( QWidget):
    valueChanged = Signal(int)
    def __init__(self):
        super(Window, self).__init__()

        self.slider =  QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)

        self.slider.setMinimum(20)
        self.slider.setMaximum(60)

        self.slider.valueChanged[int].connect(self.print_value)

        slidersLayout =  QHBoxLayout()
        slidersLayout.addWidget(self.slider)
        self.setLayout(slidersLayout)

    def print_value(self, value):
        print("value =", value)


if __name__ == '__main__':

    import sys
    app =  QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
