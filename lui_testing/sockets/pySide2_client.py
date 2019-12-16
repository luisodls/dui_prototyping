import socket
import sys
'''
from PyQt4.QtGui import (
 QWidget,
 QApplication,
 QPushButton,
 QLineEdit,
 QHBoxLayout,
)
'''

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
#from PySide2.QtWebKit import *

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.btn =  QPushButton('Go Do it', self)
        self.btn.clicked.connect(self.clickeado)

        self.lin_txt =  QLineEdit(self)

        my_box = QHBoxLayout()
        my_box.addWidget(self.btn)
        my_box.addWidget(self.lin_txt)

        my_box.addStretch()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Shell dialog')
        self.setLayout(my_box)
        self.show()


    def clickeado(self):
        shell_str = str(self.lin_txt.text())
        print("<<<... typed:", shell_str)
        self.lin_txt.setText(str(""))

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8089))

        clientsocket.send(shell_str.encode())
        clientsocket.close()


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

