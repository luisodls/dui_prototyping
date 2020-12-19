import sys, time
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

        self.window.horizontalMainLayout.addWidget(self.webEngineView)
        self.window.show()
        time.sleep(2)
        print("before load")
        self.loadPage()
        print("after load")

    def loadPage(self):
        r_g = requests.get(
            'http://localhost:8182/', stream = True, params = "a"
        )
        full_file = ''
        while True:
            tmp_dat = r_g.raw.readline()
            line_str = str(tmp_dat.decode('utf-8'))
            if line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

            else:
                full_file += line_str

        #print("html:", full_file)
        print("type(full_file):", type(full_file))
        self.webEngineView.setHtml(full_file)
        #self.webEngineView.load(full_file)

        tst_fil = open("test.html", "w")
        tst_fil.write(full_file)
        tst_fil.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainObject()
    sys.exit(app.exec_())
