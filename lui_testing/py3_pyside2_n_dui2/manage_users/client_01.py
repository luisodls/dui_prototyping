import sys, os, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2 import QtUiTools

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.window.Button1.clicked.connect(self.clicked)
        main_box = QVBoxLayout()

        self.text_out = QTextBrowser()
        main_box.addWidget(self.text_out)

        self.window.InerWidget.setLayout(main_box)
        self.window.show()

    def clicked(self):
        print("clicked")


        cmd = {"cmd_lst":["a1", "a1"]}
        print("cmd =", cmd)
        try:
            full_cmd = {"message":"something here"}
            req_post = requests.post(
                "http://127.0.0.1:45678", data = json.dumps(full_cmd)
            )
            lst_out = req_post.content
            print("lst_out =", json.loads(lst_out))

        except requests.exceptions.RequestException:
            print(
                "something went wrong with the << reset_graph >> request"
            )

        print("CommadLineEdit =", str(self.window.CommadLineEdit.text()))
        print("Data_LineEdit_01 =", str(self.window.Data_LineEdit_01.text()))
        print("Data_LineEdit_02 =", str(self.window.Data_LineEdit_02.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

