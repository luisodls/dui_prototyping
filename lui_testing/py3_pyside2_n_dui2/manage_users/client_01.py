import sys, os, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

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
        data_user = str(self.window.LineEditUser.text())
        data_pass = str(self.window.LineEditPass.text())
        print("CommadLineEdit =", command)
        print("LineEditUser =", data_user)
        print("LineEditPass =", data_pass)

        obj_dat = {
            "command":command,
            "data_user":data_user,
            "data_pass":data_pass
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

