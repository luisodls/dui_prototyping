#!/usr/bin/env python

from PySide2 import QtCore, QtWidgets, QtNetwork

class Server(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtWidgets.QLabel()

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen(address =QtNetwork.QHostAddress.Any, port = 12354):
            QtWidgets.QMessageBox.critical(self, "Counter Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        print("self.tcpServer.serverAddress()", self.tcpServer.serverAddress())

        statusLabel.setText("The server is running on port %d.\nRun the "
                "Counter Client example now." % self.tcpServer.serverPort())

        self.counting = 0

        self.tcpServer.newConnection.connect(self.sendCounting)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        self.setLayout(mainLayout)
        self.setWindowTitle("Counter Server")

    def sendCounting(self):
        print("sendCounting")
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        self.counting += 1
        counter_str = str(self.counting)

        out.writeString(counter_str)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        '''
        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)

        clientConnection.write(block)
        clientConnection.disconnectFromHost()
        '''

        self.clientConnection = self.tcpServer.nextPendingConnection()
        self.clientConnection.waitForReadyRead()
        instr = self.clientConnection.readAll()

        str_instr = str(instr, 'utf-8')
        print("Printing from server")
        print(str(str_instr))
        print("done ... Server")

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())
