import sys
import requests

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import QWebEngineView

class Example(QWidget):

    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout(self)

        self.webEngineView = QWebEngineView()
        self.loadPage()

        vbox.addWidget(self.webEngineView)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QWebEngineView')
        self.show()

    def loadPage(self):
        r_g = requests.get(
            'http://localhost:8080/', stream = True, params = "a"
        )

        full_file = ''
        line_str = ''
        while True:
            tmp_dat = r_g.raw.read(1)
            single_char = str(tmp_dat.decode('utf-8'))
            line_str += single_char
            if single_char == '\n':
                full_file += line_str
                line_str = ''

            elif line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

            print("html:", full_file)
            print("type(full_file):", type(full_file))
            self.webEngineView.setHtml(full_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

