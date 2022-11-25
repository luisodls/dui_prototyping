import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()

        OpenButton = QPushButton("\n ... Launch Open \n")
        OpenButton.clicked.connect(self.open_launch)
        mainLayout.addWidget(OpenButton)
        self.setLayout(mainLayout)

    def open_launch(self):
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
