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
    print("neither Linux or Windows")


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

        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("CLOUDRUN_ID:"))
        self.id_txt = QLineEdit()
        self.id_txt.textChanged.connect(self.line_changed)
        id_layout.addWidget(self.id_txt)
        mainLayout.addLayout(id_layout)

        project_layout = QHBoxLayout()
        project_layout.addWidget(QLabel("PROJECT:"))
        self.project_txt = QLineEdit()
        self.project_txt.textChanged.connect(self.line_changed)
        project_layout.addWidget(self.project_txt)
        mainLayout.addLayout(project_layout)

        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("TITLE:"))
        self.title_txt = QLineEdit()
        self.title_txt.textChanged.connect(self.line_changed)
        title_layout.addWidget(self.title_txt)
        mainLayout.addLayout(title_layout)

        mainLayout.addWidget(
            QLabel(
                "______________________________________________________________"
            )
        )

        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)

    def line_changed(self):
        self.data_out["url"] = str(self.url_txt.text())
        self.data_out["user"] = str(self.user_txt.text())

        tmp_id_str = str(self.id_txt.text())

        for pos_minus in [4, 9, 14]:
            if len(tmp_id_str) >= pos_minus + 1:
                if tmp_id_str[pos_minus] != "-":
                    tmp_id_str = tmp_id_str[:pos_minus] + "-" + tmp_id_str[pos_minus:]

                self.id_txt.setText(tmp_id_str)

            if len(tmp_id_str) >= pos_minus + 2:
                if tmp_id_str[pos_minus:pos_minus + 2] == "--":
                    tmp_id_str = tmp_id_str[:pos_minus] + "-" + tmp_id_str[pos_minus + 2:]

        self.id_txt.setText(tmp_id_str)

        self.data_out["id"] = tmp_id_str
        self.data_out["project"] = str(self.project_txt.text())
        self.data_out["title"] = str(self.title_txt.text())

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
