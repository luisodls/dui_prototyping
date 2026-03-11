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

        self.data_out = {}

        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_txt = QLineEdit()
        self.url_txt.textChanged.connect(self.line_changed)
        url_layout.addWidget(self.url_txt)
        mainLayout.addLayout(url_layout)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("USER:"))
        self.user_txt = QLineEdit()
        self.user_txt.textChanged.connect(self.line_changed)
        user_layout.addWidget(self.user_txt)
        mainLayout.addLayout(user_layout)


        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)

    def line_changed(self):
        self.data_out["url"] = str(self.url_txt.text())
        self.data_out["user"] = str(self.user_txt.text())

    def request_launch(self):
        print("data_out =", self.data_out)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())

guide = '''
URL         https://cloud.ccp4.ac.uk
USER        username                    # username for ccp4 cloud
CLOUDRUN_ID xxxx-xxxx-xxxx-xxxx         # cloudrun_id found in user account settings
PROJECT     dui2_project                # id of the project
TITLE       My DUI2 import project      # name of the project
TASK        import                      # use the import task
FILE  /path/to/file.mtz                 # file to upload
'''
