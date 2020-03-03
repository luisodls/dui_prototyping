from PySide2 import QtCore, QtWidgets, QtNetwork
import time
import sys
import subprocess

class CommandThread (QtCore.QThread):

    str_print_signal = QtCore.Signal(str)

    def __init__(self, parent = None):
        super(CommandThread, self).__init__()

    def set_cmd(self, cmd_in = None):
        self.cmd_to_run = cmd_in

    def run(self):
        print("... from QThread(run)")

        proc = subprocess.Popen(
            self.cmd_to_run,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        line = None
        while proc.poll() is None or line != '':
            line = proc.stdout.readline()[:-1]
            self.str_print_signal.emit(line)

        proc.stdout.close()
        print("after proc.stdout.close() ...")

class connectThread (QtCore.QThread):

    #str_print_signal = QtCore.Signal(str)

    def __init__(self, parent = None):
        super(connectThread, self).__init__()
        self.counting = 0

    def set_socket(self, socket_out = None):
        self.socket = socket_out
        print("set_socket")

    def add_str(self, new_str):
        print("new_str>>", new_str)

        #def send_str(self, str_in = "dummy str"):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_5_0)
        out.writeUInt16(0)
        self.counting += 1
        str2send = str(self.counting) + ": " + str(new_str)
        #print("from server:", str2send, "<")
        out.writeString(str2send)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        self.socket.write(block)
        time.sleep(0.01)
        self.socket.waitForBytesWritten()



    def run(self):
        print("... from QThread(run)")

        print("after proc.stdout.close() ...")


class Server(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtWidgets.QLabel()

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen(address =QtNetwork.QHostAddress.Any, port = 12354):
            QtWidgets.QMessageBox.critical(self, "DUI Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        print("self.tcpServer.serverAddress()", self.tcpServer.serverAddress())

        statusLabel.setText("The server is running on port %d.\nRun the "
                "DUI Client example now." % self.tcpServer.serverPort())

        self.counting = 0

        self.tcpServer.newConnection.connect(self.new_connection)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(statusLabel)

        send_count_butt = QtWidgets.QPushButton("send counting")
        #send_count_butt.clicked.connect(self.send_str)
        mainLayout.addWidget(send_count_butt)

        self.setLayout(mainLayout)
        self.setWindowTitle("DUI Server")

    def new_connection(self):
        self.new_socket = self.tcpServer.nextPendingConnection()
        self.new_socket.waitForReadyRead()
        self.launch_thread()
        self.new_socket.channelReadyRead.connect(self.channel_ready_read)

    def channel_ready_read(self):
        print("channel_ready_read(server)")
        self.launch_thread()

    def launch_thread(self):
        instr = self.new_socket.readAll()
        str_instr = str(instr.data().decode('utf-8'))
        print("New command: \n <<", str(str_instr), ">>")

        self.cmd_thrd = CommandThread()

        #self.cmd_thrd.str_print_signal.connect(self.cli_out)
        self.cmd_thrd.finished.connect(self.tell_finished)
        self.cmd_thrd.set_cmd(cmd_in = str_instr)

        self.cnnt_thrd = connectThread()
        #self.cnnt_thrd.finished.connect(self.tell_finished)
        #self.cnnt_thrd.str_print_signal.connect(self.cli_out)
        self.cnnt_thrd.set_socket(socket_out = self.new_socket)

        self.cmd_thrd.str_print_signal.connect(self.cnnt_thrd.add_str)
        self.cmd_thrd.start()

    def tell_finished(self):
        print("... cmd_thrd() finished")

    def cli_out(self, str_out):
        print("cli_out(", str_out, ")")
        self.send_str(str_in = str_out)

        to_move = '''
    def send_str(self, str_in = "dummy str"):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_5_0)
        out.writeUInt16(0)
        self.counting += 1
        str2send = str(self.counting) + ": " + str(str_in)
        #print("from server:", str2send, "<")
        out.writeString(str2send)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        self.new_socket.write(block)
        time.sleep(0.01)
        self.new_socket.waitForBytesWritten()
        '''


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())
