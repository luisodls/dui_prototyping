
'''
tweaked version of code copied from:

https://stackoverflow.com/questions/41167409/pyqt5-sending-and-receiving-messages-between-client-and-server
'''

import sys
from PySide2.QtCore import QByteArray, QDataStream, QIODevice
from PySide2.QtNetwork import QHostAddress, QTcpServer

from PySide2.QtGui import QTextCursor

from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit
    )

class Server(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpServer = None

        main_box = QVBoxLayout()
        self.incoming_text = QTextEdit()
        main_box.addWidget(self.incoming_text)
        low_hbox = QVBoxLayout()
        self.txt_in = QLineEdit('test text')
        low_hbox.addWidget(self.txt_in)

        send_but = QPushButton("send MSG")
        send_but.clicked.connect(self.build_msg_back)
        low_hbox.addWidget(send_but)

        main_box.addLayout(low_hbox)
        self.setLayout(main_box)

    def sessionOpened(self):
        self.tcpServer = QTcpServer(self)
        self.MyPort = 8000
        self.MyAddress = QHostAddress('127.0.0.1')
        if not self.tcpServer.listen(self.MyAddress, self.MyPort):
            print("cant listen!")
            self.close()
            return

        self.tcpServer.newConnection.connect(self.dealCommunication)

    def dealCommunication(self):
        self.clientConnection = self.tcpServer.nextPendingConnection()
        #self.clientConnection.disconnected.connect(self.clientConnection.deleteLater)
        self.clientConnection.waitForReadyRead()
        instr = self.clientConnection.readAll()

        self.incoming_text.moveCursor(QTextCursor.End)
        str_instr = str(instr, 'utf-8')
        self.incoming_text.insertPlainText( str_instr + "\n" )
        print("from server: ", str(str_instr), "<<")

    def build_msg_back(self):

        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)

        message = str(self.txt_in.text())
        print("message(server) = ", message)
        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        print("(server) out.status()", out.status())
        self.clientConnection.write(block)
        self.clientConnection.disconnectFromHost()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.sessionOpened()
    sys.exit(server.exec_())
