#!/usr/bin/env python

from PySide2 import QtCore, QtWidgets, QtNetwork

from runner import MyThread

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

        self.tcpServer.newConnection.connect(self.new_connection)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(statusLabel)

        send_count_butt = QtWidgets.QPushButton("send counting")
        send_count_butt.clicked.connect(self.send_counting)
        mainLayout.addWidget(send_count_butt)

        self.setLayout(mainLayout)
        self.setWindowTitle("Counter Server")

    def new_connection(self):
        self.new_socket = self.tcpServer.nextPendingConnection()
        self.new_socket.waitForReadyRead()
        self.print_resived_str()
        self.new_socket.channelReadyRead.connect(self.channel_ready_read)

    def channel_ready_read(self):
        print("channel_ready_read(server)")
        self.print_resived_str()

    def print_resived_str(self):
        instr = self.new_socket.readAll()

        #str_instr = str(instr, 'utf-8')
        str_instr = str(instr.data().decode('utf-8'))

        print("Printing from server")
        print("<<", str(str_instr), ">>")
        print("done ... Server")

        self.thrd = MyThread()

        self.thrd.finished.connect(self.tell_finished)
        self.thrd.str_print_signal.connect(self.cli_out)
        self.thrd.start()

    def tell_finished(self):
        print("tell_finished")

    def cli_out(self, str_out):
        print(">>: ", str_out)


    def send_counting(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        #out.setVersion(QtCore.QDataStream.Qt_5_0)
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
