import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import random

class PathButtons(QWidget):
    def __init__(self, parent = None):
        super(PathButtons, self).__init__()
        main_h_lay = QHBoxLayout()

        for tst_time in range(9):
            new_butt = QPushButton(str(tst_time) * tst_time)
            main_h_lay.addWidget(new_butt)

        self.setLayout(main_h_lay)


class PathBar(QDialog):
    def __init__(self, parent = None):
        super(PathBar, self).__init__(parent)
        mainLayout = QVBoxLayout()
        path_buttons = PathButtons(self)
        scroll_path = QScrollArea()
        scroll_path.setWidget(path_buttons)

        mainLayout.addWidget(scroll_path)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = PathBar()
    client.show()
    sys.exit(client.exec_())
