import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

def iterate(currentDir, currentItem):
    for a_file in os.listdir(currentDir):
        path = os.path.join(currentDir, a_file)
        if os.path.isdir(path):
            dirItem = QTreeWidgetItem(currentItem)
            dirItem.setText(0, a_file)
            iterate(path, dirItem)

        else:
            fileItem = QTreeWidgetItem(currentItem)
            fileItem.setText(0, a_file)


class MyTree(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTree, self).__init__(parent=parent)
        self.show()

    def fillTree(self, startDir):
        iterate(startDir, self)


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.t_view = MyTree()

        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.t_view)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)
        self.setWindowTitle("DUI front end test with HTTP")

    def request_launch(self):
        self.t_view.fillTree(
            "/scratch/dui_prototyping/lui_testing/py3_pyside2_n_dui2"
        )
        print("Launch \n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
