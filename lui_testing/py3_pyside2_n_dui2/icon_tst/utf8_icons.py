import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setGeometry(200,200, 400,400)
        self.button_all = QPushButton(
            "AAAA \n ..\u2196 \n BBBB \n ..\u2B66 \n CCCC" +
            " \n ..\u2923 \n DDDD \n ..\u2B8C \n EEEE"
        )
        self.button_all.clicked.connect(self.press_butt)

        self.button_one = QPushButton("Go Back \n\n . . \u2B8C")
        self.button_one.clicked.connect(self.press_butt)
        self_v_layout = QVBoxLayout(self)

        self_v_layout.addWidget(self.button_all)
        self_v_layout.addWidget(self.button_one)
        self_v_layout.addWidget(QLabel("click  \u2191 "))
        self.setLayout(self_v_layout)
        self.show()

    def press_butt(self):
        print("press_butt")


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = MyWidget()
    myApp.exec_()
    sys.exit(0)
