
import sys, time

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.incoming_text = QTextEdit()
        self.incoming_text.setFont(QFont("Monospace"))

        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.incoming_text)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test with HTTP")

    def request_launch(self):
        print("Launch \n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
