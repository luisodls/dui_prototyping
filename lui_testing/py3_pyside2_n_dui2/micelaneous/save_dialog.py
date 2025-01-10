from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork
import sys

class History_Box(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(History_Box, self).__init__(parent)

        self.incoming_text = QtWidgets.QTextEdit()
        self.incoming_text.setFont(QtGui.QFont("Monospace"))

        Save_Butn = QtWidgets.QPushButton("Save ...")
        Save_Butn.clicked.connect(self.requestNewConnection)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.incoming_text)
        mainLayout.addWidget(Save_Butn)
        self.setLayout(mainLayout)
        self.setWindowTitle("Show history as a script")

    def requestNewConnection(self):
        print("here")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    H_Box = History_Box()
    H_Box.show()
    sys.exit(H_Box.exec_())
