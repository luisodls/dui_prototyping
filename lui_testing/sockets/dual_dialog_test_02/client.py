
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
        self.tcpSocket.readyRead.connect(self.dealCommunication)
        self.tcpSocket.stateChanged.connect(self.state_changed)
        self.tcpSocket.error.connect(self.displayError)
        #self.tcpSocket.disconnected.connect(self.makeRequest)
        self.blockSize = 0

        main_box = QVBoxLayout()
        self.incoming_text = QTextEdit()
        main_box.addWidget(self.incoming_text)
        low_hbox = QVBoxLayout()
        self.txt_in = QLineEdit('test text')
        low_hbox.addWidget(self.txt_in)
        send_but = QPushButton("send MSG")

        send_but.clicked.connect(self.build_request)
        #self.makeRequest()  #

        low_hbox.addWidget(send_but)
        main_box.addLayout(low_hbox)
        self.setLayout(main_box)

    def state_changed(self, state):
        print("client(state_changed)")
        print("type(state): ", type(state))
        '''
        print("dir(state)", dir(state))
        print("state.BoundState       ", state.BoundState       )
        print("state.ClosingState     ", state.ClosingState     )
        print("state.ConnectedState   ", state.ConnectedState   )
        print("state.ConnectingState  ", state.ConnectingState  )
        print("state.HostLookupState  ", state.HostLookupState  )
        print("state.ListeningState   ", state.ListeningState   )
        print("state.UnconnectedState ", state.UnconnectedState )
        print("state.values", state.values)

        '''

        print("state.name", state.name)

        #print("\n self.tcpSocket.state(): ", self.tcpSocket.state())

    def build_request(self):
        txt2send = str.encode(self.txt_in.text())
        self.makeRequest()
        self.tcpSocket.write(txt2send)

    def makeRequest(self):
        HOST = '127.0.0.1'
        PORT = 8000
        try:
            self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)
            self.tcpSocket.waitForConnected(1000)

        except:
            print("failed attempt to connect from client")


    def dealCommunication(self):

        self.tcpSocket.waitForConnected(1000) ###

        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)

        self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            print("self.tcpSocket.bytesAvailable() < self.blockSize")
            return

        self.incoming_text.moveCursor(QTextCursor.End)
        read_str = instr.readString()
        str_instr = str(read_str)
        self.incoming_text.insertPlainText(str_instr + "\n")

        print("from client: ", str_instr, "<<")

        self.makeRequest()

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass

        else:
            print(self, "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
