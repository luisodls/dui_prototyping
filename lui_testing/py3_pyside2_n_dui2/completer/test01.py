import sys, time
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")


        wordList = ["alpha", "omega", "omicron", "zeta"]
        completer = QCompleter(wordList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.window.lineEdit_in.setCompleter(completer)

        self.window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

