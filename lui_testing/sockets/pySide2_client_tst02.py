#import socket
import sys

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.manager = QNetworkAccessManager(self)
        self.manager.finished[QNetworkReply].connect(self.replyFinished)
        self.manager.sslErrors.connect(self.errorSsl)

        print(dir(self.manager))


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

        tmp_off = '''
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8089))

        clientsocket.send(shell_str.encode())
        clientsocket.close()
        '''

        #self.manager.get(QNetworkRequest(QUrl("localhost:8089")))
        #self.manager.post(QNetworkRequest(QUrl("localhost:8089")), shell_str.encode())

        self.manager.put(QNetworkRequest(QUrl("localhost:8089")), shell_str.encode())

    def readReady(self):
        print(Example.readReady)

    def errorSsl(self, rep):
        print("Example.errorSsl")

    def replyFinished(self, rep):
        rep.readyRead.connect(self.readReady)
        print("rep.error()=", rep.error())
        print("rep=", rep)
        print("rep.NetworkError: ", rep.NetworkError())
        '''
        er = rep.error()
        if er == QNetworkReply.NoError:
            print("NoError")

        else:
            print("E R R O R")
            print("rep.NetworkError: ", rep.NetworkError())
        '''
        bytes_string = rep.readAll()

        print("str:" + str(bytes_string) + ">>")


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

