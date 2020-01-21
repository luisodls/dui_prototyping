
'''
tweaked version of code copied from:

https://stackoverflow.com/questions/41167409/pyqt5-sending-and-receiving-messages-between-client-and-server
'''

import sys
from PySide2.QtNetwork import QTcpSocket, QAbstractSocket
from PySide2.QtGui import QTextCursor

from PySide2.QtCore import (
    QDataStream,
    QIODevice
    )

from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit
    )

class Client(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpSocket = QTcpSocket(self)
        self.blockSize = 0

        main_box = QVBoxLayout()

        self.incoming_text = QTextEdit()
        main_box.addWidget(self.incoming_text)

        low_hbox = QVBoxLayout()

        self.txt_in = QLineEdit('test text')
        low_hbox.addWidget(self.txt_in)

        send_but = QPushButton("send MSG")
        send_but.clicked.connect(self.build_request)
        low_hbox.addWidget(send_but)

        main_box.addLayout(low_hbox)

        self.setLayout(main_box)


    def build_request(self):
        txt2send = str.encode(self.txt_in.text())
        self.makeRequest()
        self.tcpSocket.write(txt2send)
        self.tcpSocket.readyRead.connect(self.dealCommunication)
        self.tcpSocket.error.connect(self.displayError)

    def makeRequest(self):
        HOST = '127.0.0.1'
        PORT = 8000
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)
        self.tcpSocket.waitForConnected(1000)

    def dealCommunication(self):
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return

        self.incoming_text.moveCursor(QTextCursor.End)
        str_instr = str(instr.readString())
        self.incoming_text.insertPlainText(str_instr + "\n")

        print("Printing from client")
        print(str_instr)
        print("done ... Client")

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass

        else:
            print(self, "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
