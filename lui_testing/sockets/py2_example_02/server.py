#!/usr/bin/env python

from __future__ import division, print_function
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

class Server( QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel =  QLabel()

        self.tcpServer =  QTcpServer(self)
        if not self.tcpServer.listen(address = QHostAddress.Any, port = 12354):
            QMessageBox.critical(self, "Counter Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        print("self.tcpServer.serverAddress()", self.tcpServer.serverAddress())

        statusLabel.setText("The server is running on port %d.\nRun the "
                "Counter Client example now." % self.tcpServer.serverPort())

        self.counting = 0

        self.tcpServer.newConnection.connect(self.new_connection)
        mainLayout =  QVBoxLayout()
        mainLayout.addWidget(statusLabel)

        send_count_butt =  QPushButton("send counting")
        send_count_butt.clicked.connect(self.send_counting)
        mainLayout.addWidget(send_count_butt)

        self.setLayout(mainLayout)
        self.setWindowTitle("Counter Server")

    def new_connection(self):
        self.new_socket = self.tcpServer.nextPendingConnection()
        self.new_socket.waitForReadyRead()
        self.print_resived_str()
        #self.new_socket.channelReadyRead.connect(self.channel_ready_read)
        self.new_socket.readyRead.connect(self.channel_ready_read)

    def channel_ready_read(self):
        print("channel_ready_read(server)")
        self.print_resived_str()

    def print_resived_str(self):
        instr = self.new_socket.readAll()

        str_instr = str(instr)
        print("Printing from server")
        print("<<", str(str_instr), ">>")
        print("done ... Server")


    def send_counting(self):
        block =  QByteArray()
        out =  QDataStream(block,  QIODevice.ReadWrite)
        #out.setVersion( QDataStream.Qt_5_0)
        out.writeUInt16(0)
        self.counting += 1
        counter_str = "number of clicks =" + str(self.counting) + " so far"
        out.writeString(counter_str)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        self.new_socket.write(block)


if __name__ == '__main__':

    import sys

    app =  QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())
