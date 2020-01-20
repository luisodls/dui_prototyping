
'''
tweaked version of code copied from:

https://stackoverflow.com/questions/41167409/pyqt5-sending-and-receiving-messages-between-client-and-server
'''

import sys
from PySide2.QtCore import QByteArray, QDataStream, QIODevice
from PySide2.QtWidgets import QApplication, QDialog
from PySide2.QtNetwork import QHostAddress, QTcpServer

class Server(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpServer = None

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
        clientConnection = self.tcpServer.nextPendingConnection()
        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)

        message = "Goodbye!"
        message = str(message)

        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        clientConnection.waitForReadyRead()
        instr = clientConnection.readAll()

        print("Printing from server")
        print(str(instr, encoding='ascii'))
        print("done ... Server")

        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.write(block)
        clientConnection.disconnectFromHost()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.sessionOpened()
    sys.exit(server.exec_())
