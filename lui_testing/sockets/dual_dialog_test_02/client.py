#!/usr/bin/env python

from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.dataLineEdit = QtWidgets.QLineEdit('test text')
        self.incoming_text = QtWidgets.QTextEdit()
        self.Talk2serverButton = QtWidgets.QPushButton("send to server")

        self.tcpSocket = QtNetwork.QTcpSocket(self)

        self.Talk2serverButton.clicked.connect(self.requestNewConnection)
        self.tcpSocket.readyRead.connect(self.readFromServer)
        self.tcpSocket.error.connect(self.displayError)
        self.tcpSocket.stateChanged.connect(self.tell_State)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.incoming_text)
        mainLayout.addWidget(QtWidgets.QLabel("Type here"))
        mainLayout.addWidget(self.dataLineEdit)
        mainLayout.addWidget(self.Talk2serverButton)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")

    def tell_State(self):
        print("self.tcpSocket.state()", self.tcpSocket.state())
        print("self.tcpSocket.isValid()", self.tcpSocket.isValid())

    def requestNewConnection(self):
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(QtNetwork.QHostAddress.Any, 12354, QtCore.QIODevice.ReadWrite)

        if self.tcpSocket.waitForConnected(1000):
            print("Connected!")

        txt2send = str.encode(self.dataLineEdit.text())
        self.tcpSocket.write(txt2send)

    def readFromServer(self):
        print("client.readFromServer")
        instr = QtCore.QDataStream(self.tcpSocket)
        instr.setVersion(QtCore.QDataStream.Qt_5_0)

        self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            print("tcpSocket.bytesAvailable() < self.blockSize")
            return

        nxt_count = instr.readString()
        print("nxt_count(client) =", nxt_count)
        self.incoming_text.moveCursor(QtGui.QTextCursor.End)
        self.incoming_text.insertPlainText(nxt_count + "\n")

    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtWidgets.QMessageBox.information(self, " Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtWidgets.QMessageBox.information(self, " Client",
                    "The connection was refused by the peer. Make sure "
                    "the server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QtWidgets.QMessageBox.information(self, " Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
