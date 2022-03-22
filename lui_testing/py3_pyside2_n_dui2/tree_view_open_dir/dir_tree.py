
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import os, sys

class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "simple.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI Cloud")

        self.mod = QFileSystemModel()
        self.mod.setRootPath(QDir.homePath())

        self.tree_vw =  QTreeView()
        self.tree_vw.setModel(self.mod)
        self.window.verticalLayout.addWidget(self.tree_vw)

        self.tree_vw.clicked.connect(self.someting_click)
        self.window.show()

    def someting_click(self, event):
        index = self.tree_vw.currentIndex()
        #print("\n\n dir(self.tree_vw) = ", dir(self.tree_vw), "\n")
        print("\n\n index =", index)
        #print("dir(self.mod) = ", dir(self.mod))
        new_path = self.mod.filePath(index)
        new_name = self.mod.fileName(index)
        new_info = self.mod.fileInfo(index)
        print("new_path =", new_path)
        print("new_name =", new_name)
        print("new_info.isDir =", new_info.isDir())
        print("new_info.isFile =", new_info.isFile())

if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()
    sys.exit(app.exec_())
