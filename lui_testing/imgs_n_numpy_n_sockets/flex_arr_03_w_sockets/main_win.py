import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from PySide2 import QtUiTools

class Form(QObject):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.window = QtUiTools.QUiLoader().load("my_win.ui")
        self.window.LoadButton.clicked.connect(self.btn_clk)

        self.my_scene_1 = QGraphicsScene()
        self.window.graphicsView.setScene(self.my_scene_1)
        self.window.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)

        print("QGraphicsScenes ready")
        self.window.show()

    def btn_clk(self):
        print("self.btn_clk start")

        fileName = "../../PyQt4_toys/tux_n_chrome.png"
        image1 = QImage(fileName)
        self.pixmap = QPixmap.fromImage(image1)

        self.my_scene_1.addPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

