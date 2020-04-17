from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork
import sys, time
import requests

class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.incoming_text = QtWidgets.QTextEdit()
        self.incoming_text.setFont(QtGui.QFont("Monospace"))
        self.dataLineEdit = QtWidgets.QLineEdit()

        self.dataLineEdit.setPlaceholderText("Type command")

        self.dataLineEdit.setFont(QtGui.QFont("Monospace"))

        send2serverButton = QtWidgets.QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.incoming_text)
        mainLayout.addWidget(QtWidgets.QLabel(" \n Type here"))
        mainLayout.addWidget(self.dataLineEdit)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test")

    def request_launch(self):

        cmd_str = str.encode(self.dataLineEdit.text())

        print('entered:', cmd_str)
        cmd = {'command': [cmd_str]}
        r_g = requests.get('http://localhost:8080/', stream = True, params = cmd)

        line_str = ''
        while True:
            tmp_dat = r_g.raw.read(1)
            single_char = str(tmp_dat.decode('utf-8'))
            line_str += single_char
            if single_char == '\n':
                print(line_str[:-1])
                self.incoming_text.moveCursor(QtGui.QTextCursor.End)
                self.incoming_text.insertPlainText(line_str)
                line_str = ''

            elif line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())



