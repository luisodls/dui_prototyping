import sys

try:
    #from PySide6.QtWebEngineWidgets import QWebEngineView
    #from PySide6.QtWebEngineCore import QWebEngineSettings
    from PySide6 import QtUiTools
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    print("Using PySide6 as Qt bindings")

except ModuleNotFoundError:
    #from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PySide2 import QtUiTools
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    print("Using PySide2 as Qt bindings")


import os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"


class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")
        self.window.Button1.clicked.connect(self.clicked)
        self.window.show()

    def clicked(self):
        print("clicked")

        dlg = QMessageBox()
        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a question dialog")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Yes !")
        else:
            print("Cancel !")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

