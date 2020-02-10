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
        str_instr = str(instr.data().decode('utf-8'))
        print("Printing from server")
        print("<<", str(str_instr), ">>")

        self.thrd = MyThread()
        self.thrd.finished.connect(self.tell_finished)
        self.thrd.str_print_signal.connect(self.cli_out)
        self.thrd.start()

    def tell_finished(self):
        print("tell_finished")

    def cli_out(self, str_out):
        self.send_counting(str_in = str_out)

    def send_counting(self, str_in = "dummy str"):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_5_0)
        out.writeUInt16(0)
        self.counting += 1
        str2send = str(self.counting) + ": " + str(str_in)
        print("from server:", str2send, "<")
        out.writeString(str2send)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)


        self.new_socket.write(block)
        for ntimes in range(500):
            print("ntimes:", ntimes)
            print("self.new_socket.state()", self.new_socket.state())
            self.new_socket.waitForBytesWritten()

        #print("dir(block): ", dir(block))
        print("type(block.capacity)              ",type(block.capacity)              )
        print("type(block.cbegin)                ",type(block.cbegin)                )
        print("type(block.cend)                  ",type(block.cend)                  )
        print("type(block.chop)                  ",type(block.chop)                  )
        print("type(block.clear)                 ",type(block.clear)                 )
        print("type(block.contains)              ",type(block.contains)              )
        print("type(block.count)                 ",type(block.count)                 )
        print("type(block.data)                  ",type(block.data)                  )
        print("type(block.endsWith)              ",type(block.endsWith)              )
        print("type(block.fill)                  ",type(block.fill)                  )
        print("type(block.fromBase64)            ",type(block.fromBase64)            )
        print("type(block.fromHex)               ",type(block.fromHex)               )
        print("type(block.fromPercentEncoding)   ",type(block.fromPercentEncoding)   )
        print("type(block.fromRawData)           ",type(block.fromRawData)           )
        print("type(block.indexOf)               ",type(block.indexOf)               )
        print("type(block.insert)                ",type(block.insert)                )
        print("type(block.isEmpty)               ",type(block.isEmpty)               )
        print("type(block.isNull)                ",type(block.isNull)                )
        print("type(block.isSharedWith)          ",type(block.isSharedWith)          )
        print("type(block.lastIndexOf)           ",type(block.lastIndexOf)           )
        print("type(block.left)                  ",type(block.left)                  )
        print("type(block.leftJustified)         ",type(block.leftJustified)         )
        print("type(block.length)                ",type(block.length)                )
        print("type(block.mid)                   ",type(block.mid)                   )
        print("type(block.number)                ",type(block.number)                )
        print("type(block.prepend)               ",type(block.prepend)               )
        print("type(block.remove)                ",type(block.remove)                )
        print("type(block.repeated)              ",type(block.repeated)              )
        print("type(block.replace)               ",type(block.replace)               )
        print("type(block.reserve)               ",type(block.reserve)               )
        print("type(block.resize)                ",type(block.resize)                )
        print("type(block.right)                 ",type(block.right)                 )
        print("type(block.rightJustified)        ",type(block.rightJustified)        )
        print("type(block.setNum)                ",type(block.setNum)                )
        print("type(block.setRawData)            ",type(block.setRawData)            )
        print("type(block.simplified)            ",type(block.simplified)            )
        print("type(block.size)                  ",type(block.size)                  )
        print("type(block.split)                 ",type(block.split)                 )
        print("type(block.squeeze)               ",type(block.squeeze)               )
        print("type(block.startsWith)            ",type(block.startsWith)            )
        print("type(block.swap)                  ",type(block.swap)                  )
        print("type(block.toBase64)              ",type(block.toBase64)              )
        print("type(block.toDouble)              ",type(block.toDouble)              )
        print("type(block.toFloat)               ",type(block.toFloat)               )
        print("type(block.toHex)                 ",type(block.toHex)                 )
        print("type(block.toInt)                 ",type(block.toInt)                 )
        print("type(block.toLong)                ",type(block.toLong)                )
        print("type(block.toLongLong)            ",type(block.toLongLong)            )
        print("type(block.toLower)               ",type(block.toLower)               )
        print("type(block.toPercentEncoding)     ",type(block.toPercentEncoding)     )
        print("type(block.toShort)               ",type(block.toShort)               )
        print("type(block.toUInt)                ",type(block.toUInt)                )
        print("type(block.toULong)               ",type(block.toULong)               )
        print("type(block.toULongLong)           ",type(block.toULongLong)           )
        print("type(block.toUShort)              ",type(block.toUShort)              )
        print("type(block.toUpper)               ",type(block.toUpper)               )
        print("type(block.trimmed)               ",type(block.trimmed)               )
        print("type(block.truncate)              ",type(block.truncate)              )


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    server = Server()
    sys.exit(server.exec_())
