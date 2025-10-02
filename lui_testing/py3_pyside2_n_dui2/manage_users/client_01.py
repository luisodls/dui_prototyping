import sys, os, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")
        self.window.PostButton.clicked.connect(self.post_clicked)

        self.window.GetButton.clicked.connect(self.get_clicked)

        self.window.show()

    def post_clicked(self):

        self.window.TextOut.append("Post clicked")

        command = str(self.window.PostCommadEdit.text())
        data_user = str(self.window.LineEditUser.text())
        data_pass = str(self.window.LineEditPass.text())
        print("PostCommadEdit =", command)
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
            self.window.TextOut.append("lst_out =" + str(json.loads(lst_out)))

        except requests.exceptions.RequestException:
            self.window.TextOut.append(
                "something went wrong  << RequestException >> "
            )

        except json.decoder.JSONDecodeError:
            self.window.TextOut.append(
                "something went wrong  << JSONDecodeError >> "
            )

    def get_clicked(self):
        self.window.TextOut.append("Get clicked")
        command = str(self.window.GetCommadEdit.text())
        data_token = str(self.window.LineEditToken.text())
        print("GetCommadEdit =", command)
        print("LineEditToken =", data_token)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

