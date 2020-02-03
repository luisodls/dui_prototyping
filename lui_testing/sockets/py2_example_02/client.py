#!/usr/bin/env python

from __future__ import division, print_function
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

class Client( QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.incoming_text =  QTextEdit()
        self.dataLineEdit =  QLineEdit('test text')
        send2serverButton =  QPushButton("send to server")

        self.tcpSocket =  QTcpSocket(self)

        send2serverButton.clicked.connect(self.requestNewConnection)
        self.tcpSocket.readyRead.connect(self.readFromServer)
        self.tcpSocket.error.connect(self.displayError)

        mainLayout =  QVBoxLayout()
        mainLayout.addWidget(self.incoming_text)
        mainLayout.addWidget( QLabel(" \n Type here"))
        mainLayout.addWidget(self.dataLineEdit)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("Fortune Client")

        self.tcpSocket.stateChanged.connect(self.tell_State)

    def tell_State(self):
        print("self.tcpSocket.state()", self.tcpSocket.state())
        print("self.tcpSocket.isValid()", self.tcpSocket.isValid())

    def requestNewConnection(self):
        if not self.tcpSocket.isValid():
            self.tcpSocket.abort()
            self.tcpSocket.connectToHost( QHostAddress.Any, 12354,  QIODevice.ReadWrite)

        if self.tcpSocket.waitForConnected(1000):
            print("Connected!")

        else:
            print("Failed to connect")

        txt2send = str(self.dataLineEdit.text())
        #txt2send = str.encode(self.dataLineEdit.text())
        self.tcpSocket.write(txt2send)

    def readFromServer(self):
        print("client.readFromServer")
        InStr =  QDataStream(self.tcpSocket)
        #InStr.setVersion( QDataStream.Qt_5_0)

        blockSize = InStr.readUInt16()

        if self.tcpSocket.bytesAvailable() < blockSize:
            print("tcpSocket.bytesAvailable() < blockSize")
            return

        nxt_str = InStr.readString()
        print("nxt_str(client) =", nxt_str)
        self.incoming_text.moveCursor(QTextCursor.End)
        self.incoming_text.insertPlainText(nxt_str + "\n")

    def displayError(self, socketError):
        if socketError ==  QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError ==  QAbstractSocket.HostNotFoundError:
             QMessageBox.information(self, " Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError ==  QAbstractSocket.ConnectionRefusedError:
             QMessageBox.information(self, " Client",
                    "The connection was refused by the peer. Make sure "
                    "the server is running, and check that the host name "
                    "and port settings are correct.")
        else:
             QMessageBox.information(self, " Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':

    import sys

    app =  QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
