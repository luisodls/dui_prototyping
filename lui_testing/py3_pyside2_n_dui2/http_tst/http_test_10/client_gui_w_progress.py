import sys

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

        self.webEngineView.loadStarted.connect(self.load_started)
        self.webEngineView.loadProgress.connect(self.load_progress)
        self.webEngineView.loadFinished.connect(self.load_finished)

        self.loadPage()

        self.window.horizontalMainLayout.addWidget(self.webEngineView)
        self.window.show()

    def loadPage(self):
        f_name = "report2.html"

        with open(f_name, 'r') as f:
            html = f.read()
            print("type(html) =", type(html))
            self.webEngineView.setHtml(html)

    def load_started(self):
        print("load_started")

    def load_progress(self, progress):
        print("load_progress:", progress)

    def load_finished(self):
        print("load_finished")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainObject()
    sys.exit(app.exec_())
