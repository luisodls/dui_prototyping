import sys
#from PySide import QtUiTools
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2 import QtUiTools

class Form(QObject):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.window = QtUiTools.QUiLoader().load("my_win.ui")
        self.window.pushButton.clicked.connect(self.btn_clk)

        self.my_scene_1 = QGraphicsScene()
        self.window.graphicsView_1.setScene(self.my_scene_1)
        self.window.graphicsView_1.setDragMode(QGraphicsView.ScrollHandDrag)

        self.my_scene_2 = QGraphicsScene()
        self.window.graphicsView_2.setScene(self.my_scene_2)
        self.window.graphicsView_2.setDragMode(QGraphicsView.ScrollHandDrag)

        print("QGraphicsScenes ready")

        print("dir(self.my_scene_1);", dir(self.my_scene_1))
        self.window.show()

    def btn_clk(self):
        print("self.btn_clk start")

        fileName = "../../PyQt4_toys/tux_n_chrome.png"
        image1 = QImage(fileName)
        fileName = "../../PyQt4_toys/tux_n_chrome.png"
        image2 = QImage(fileName)
        self.pixmap_1 = QPixmap.fromImage(image1)
        self.pixmap_2 = QPixmap.fromImage(image2)

        self.my_scene_1.addPixmap(self.pixmap_1)
        self.my_scene_2.addPixmap(self.pixmap_2)

        print("dir(self.pixmap_1);", dir(self.pixmap_1))

        print("self.btn_clk end")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

