#!/usr/bin/env python

from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.blockSize = 0
        self.currentFortune = ''

        DataInLabel = QtWidgets.QLabel("Type here")
        self.dataLineEdit = QtWidgets.QLineEdit('test text')

        self.statusLabel = QtWidgets.QLabel("This examples requires that you run "
                "the Server example as well.")

        self.Talk2serverButton = QtWidgets.QPushButton("send to server")

        self.tcpSocket = QtNetwork.QTcpSocket(self)

        self.Talk2serverButton.clicked.connect(self.requestNewFortune)
        self.tcpSocket.readyRead.connect(self.readFortune)
        self.tcpSocket.error.connect(self.displayError)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(DataInLabel, 0, 0)
        mainLayout.addWidget(self.dataLineEdit, 0, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(self.Talk2serverButton, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")

    def requestNewFortune(self):
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(QtNetwork.QHostAddress.Any, 12354)

    def readFortune(self):
        instr = QtCore.QDataStream(self.tcpSocket)
        instr.setVersion(QtCore.QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return

        nextFortune = instr.readString()

        try:
            # Python v3.
            nextFortune = str(nextFortune, encoding='ascii')
        except TypeError:
            # Python v2.
            pass

        if nextFortune == self.currentFortune:
            QtCore.QTimer.singleShot(0, self.requestNewFortune)
            return

        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)

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
