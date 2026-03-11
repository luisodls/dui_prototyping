import sys, os, platform
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


if platform.system() == "Windows":
    print("running on Windows")
    win_str = "true"

elif platform.system() == "Linux":
    print("running on Linux")
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ["WAYLAND_DISPLAY"] = ""

else:
    print("nether Linux or Windows")


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()


        self.url_txt = QLineEdit()
        self.url_txt.textChanged.connect(self.line_changed)

        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)

    def line_changed(self):
        ext_par = str(self.url_txt.text())
        print("ext_par =", ext_par)

    def request_launch(self):
        print("Launch \n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())


URL         https://cloud.ccp4.ac.uk
USER        username                    # username for ccp4 cloud
CLOUDRUN_ID xxxx-xxxx-xxxx-xxxx         # cloudrun_id found in user account settings
PROJECT     dui2_project                # id of the project
TITLE       My DUI2 import project      # name of the project
TASK        import                      # use the import task
FILE  /path/to/file.mtz                 # file to upload
