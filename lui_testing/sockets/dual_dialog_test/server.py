
'''
tweaked version of code copied from:

https://stackoverflow.com/questions/41167409/pyqt5-sending-and-receiving-messages-between-client-and-server
'''

import sys
from PySide2.QtCore import QByteArray, QDataStream, QIODevice
from PySide2.QtNetwork import QHostAddress, QTcpServer
from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLineEdit
    )

class Server(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpServer = None

        mainbox = QVBoxLayout()

        self.txt_in = QLineEdit('test text')
        mainbox.addWidget(self.txt_in)

        send_but = QPushButton("send MSG")
        send_but.clicked.connect(self.build_msg_back)
        mainbox.addWidget(send_but)

        self.setLayout(mainbox)


    def sessionOpened(self):
        self.tcpServer = QTcpServer(self)
        PORT = 8000
        address = QHostAddress('127.0.0.1')
        if not self.tcpServer.listen(address, PORT):
            print("cant listen!")
            self.close()
            return

        self.tcpServer.newConnection.connect(self.dealCommunication)

    def dealCommunication(self):
        self.clientConnection = self.tcpServer.nextPendingConnection()
        self.clientConnection.waitForReadyRead()
        instr = self.clientConnection.readAll()

        print("Printing from server")
        print(str(instr, encoding='ascii'))
        print("done ... Server")

    def build_msg_back(self):

        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)

        message = str(self.txt_in.text())

        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)


        self.clientConnection.disconnected.connect(self.clientConnection.deleteLater)
        self.clientConnection.write(block)
        self.clientConnection.disconnectFromHost()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.sessionOpened()
    sys.exit(server.exec_())
