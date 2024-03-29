from writing import imprime_algo
from in_dir.write_from_dir import lee_un_fichero

import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2 import QtUiTools

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)


        ui_dir_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = ui_dir_path + os.sep + "rec_n1/simple.ui"
        print("ui_path =" + ui_path)
        self.window = QtUiTools.QUiLoader().load(ui_path)


        #self.window = QtUiTools.QUiLoader().load("rec_n1/simple.ui")

        self.window.Button1.clicked.connect(self.clicked)
        self.html_view = QWebEngineView()

        main_box = QVBoxLayout()
        main_box.addWidget(self.html_view)

        self.window.InerWidget.setLayout(main_box)
        self.window.show()

    def clicked(self):
        print("clicked")
        abs_path = str(os.path.dirname(os.path.abspath(__file__)))
        html_path = abs_path + "/in_dir/res_txt/dummy.html"
        print("html_path =", html_path)

        self.html_view.load(QUrl.fromLocalFile(html_path))
        self.html_view.show()


def main():
    print("tst 7 tmp")
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
