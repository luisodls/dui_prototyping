#!/usr/bin/env python

from PySide2 import QtCore, QtWidgets, QtNetwork

class Server(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtWidgets.QLabel()

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen(address =QtNetwork.QHostAddress.Any, port = 12354):
            QtWidgets.QMessageBox.critical(self, "dui2 Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        print("self.tcpServer.serverAddress()", self.tcpServer.serverAddress())

        statusLabel.setText("The server is running on port %d.\nRun the "
                "Counter Client example now." % self.tcpServer.serverPort())

        self.counting = 0

        self.tcpServer.newConnection.connect(self.reseived_str)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(statusLabel)

        send_count_butt = QtWidgets.QPushButton("send counting")
        send_count_butt.clicked.connect(self.sendCounting)
        mainLayout.addWidget(send_count_butt)

        self.setLayout(mainLayout)
        self.setWindowTitle("dui2 Server")

    def reseived_str(self):
        self.new_socket = self.tcpServer.nextPendingConnection()
        self.new_socket.waitForReadyRead()
        instr = self.new_socket.readAll()

        str_instr = str(instr, 'utf-8')
        print("Printing from server")
        print("<<", str(str_instr), ">>")
        print("done ... Server")

    def sendCounting(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_5_0)
        out.writeUInt16(0)
        self.counting += 1
        counter_str = "number of clicks =" + str(self.counting) + " so far"
        out.writeString(counter_str)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        self.new_socket.write(block)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())
