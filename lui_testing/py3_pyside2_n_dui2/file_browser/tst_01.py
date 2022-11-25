import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()

        OpenButton = QPushButton("\n ... Open file \n")
        OpenButton.clicked.connect(self.open_file)
        mainLayout.addWidget(OpenButton)

        DirButton = QPushButton("\n ... Open Dir \n")
        DirButton.clicked.connect(self.open_dir)
        mainLayout.addWidget(DirButton)

        self.setLayout(mainLayout)

    def open_file(self):
        print("Launch \n")


        try:
            file_in_path = QFileDialog.getOpenFileName(
                parent = self,
                caption = "Open Image File",
                dir = "/",
                filter = "Files (*.*)"
            )[0]

            print("Opened:", str(file_in_path))

        except FileNotFoundError:
            print("No file selected")

    def open_dir(self):

        new_dir = QFileDialog.getExistingDirectory(
            parent = self,
            caption = "Open Directory", dir = "/home"
        )
        print("Opened:", new_dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
