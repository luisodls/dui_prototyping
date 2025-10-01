import sys, os, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2 import QtUiTools

import hashlib
import secrets
import getpass
from datetime import datetime


os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.window.Button1.clicked.connect(self.clicked)
        main_box = QVBoxLayout()

        self.text_out = QTextEdit()
        main_box.addWidget(self.text_out)

        self.window.InerWidget.setLayout(main_box)
        self.window.show()

    def clicked(self):
        command = str(self.window.CommadLineEdit.text())
        data1 = str(self.window.Data_LineEdit_01.text())
        data2 = str(self.window.Data_LineEdit_02.text())
        print("CommadLineEdit =", command)
        print("Data_LineEdit_01 =", data1)
        print("Data_LineEdit_02 =", data2)

        obj_dat = {
            "command":command,
            "data1":data1,
            "data2":data2
        }
        print("obj_dat =", obj_dat)
        try:
            req_post = requests.post(
                "http://127.0.0.1:45678", data = json.dumps(obj_dat)
            )
            lst_out = req_post.content
            #print("lst_out =", json.loads(lst_out))
            self.text_out.append("lst_out =" + str(json.loads(lst_out)))

        except requests.exceptions.RequestException:
            print(
                "something went wrong  << RequestException >> "
            )

        except json.decoder.JSONDecodeError:
            print(
                "something went wrong  << JSONDecodeError >> "
            )

        self.text_out.append("clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

