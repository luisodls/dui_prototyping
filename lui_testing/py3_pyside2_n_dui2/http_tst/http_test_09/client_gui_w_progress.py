import sys
import requests

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2 import QtUiTools


class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)

        self.window = QtUiTools.QUiLoader().load("viewer.ui")
        self.webEngineView = QWebEngineView()
        self.loadPage()

        self.window.horizontalMainLayout.addWidget(self.webEngineView)
        self.window.show()

    def loadPage(self):
        f_name = "report2.html"

        with open(f_name, 'r') as f:
            html = f.read()
            print("type(html) =", type(html))
            self.webEngineView.setHtml(html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainObject()
    sys.exit(app.exec_())

