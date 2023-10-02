import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2 import QtUiTools

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.window.Button1.clicked.connect(self.clicked)
        self.html_view = QWebEngineView()

        main_box = QVBoxLayout()
        main_box.addWidget(self.html_view)
        #main_box.addWidget(QLabel("Testing"))

        self.window.InerWidget.setLayout(main_box)
        self.window.show()

    def clicked(self):
        print("clicked")
        self.html_view.load(QUrl("http://qt-project.org/"))
        '''self.html_view.load(
            QUrl.fromLocalFile(
                "/home/luiso/dui_dev/dui_prototyping/lui_testing/data4test/report_node_3.html"
            )
        )'''

        self.html_view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

