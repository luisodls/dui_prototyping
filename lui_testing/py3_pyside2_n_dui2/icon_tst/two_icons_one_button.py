import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class imgButton(QPushButton):
    def __init__(self, parent = None):
        super(imgButton, self).__init__(parent)
        hor_low_lay = QHBoxLayout(self)

        DirPixMapi = getattr(QStyle, 'SP_DirIcon')
        FilePixMapi = getattr(QStyle, 'SP_ArrowUp')
        tmp_ico = self.style().standardIcon(DirPixMapi)
        tmp_ico1 = self.style().standardIcon(FilePixMapi)
        tmp_lab = QLabel()
        tmp_lab.setPixmap(tmp_ico.pixmap(tmp_ico.actualSize(QSize(48, 48))))
        hor_low_lay.addWidget(tmp_lab)
        tmp_lab1 = QLabel()
        tmp_lab1.setPixmap(tmp_ico1.pixmap(tmp_ico1.actualSize(QSize(48, 48))))
        hor_low_lay.addWidget(tmp_lab1)

        ver_top_lay = QVBoxLayout()
        ver_top_lay.addWidget(QLabel("Dir Up"))
        ver_top_lay.addLayout(hor_low_lay)
        self.setLayout(ver_top_lay)

        print("\n", tmp_ico.availableSizes(), "\n")
        print("\n", tmp_ico1.availableSizes(), "\n")


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setGeometry(200,200, 400,400)
        self.button = imgButton(self)
        self.button.clicked.connect(self.press_butt)
        self_v_layout = QVBoxLayout(self)
        self_v_layout.addWidget(self.button)
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
