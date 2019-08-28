
import sys
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "test02.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.my_scene_1 = QtGui.QGraphicsScene()
        self.graphicsView_1.setScene(self.my_scene_1)

        self.my_scene_2 = QtGui.QGraphicsScene()
        self.graphicsView_2.setScene(self.my_scene_2)

        self.pushButton_1.clicked.connect(self.set_img_1)
        self.pushButton_2.clicked.connect(self.set_img_2)

        self.setLayout(self.gridLayout)
        self.setWindowTitle('Testing')
        self.show()

    def set_img_1(self):
        print "Hi ..."

        fileName = "/home/ufn91840/M_Pics/chihuahua.png"
        image = QtGui.QImage(fileName)
        tmp_pixmap = QtGui.QPixmap.fromImage(image)
        self.my_scene_1.addPixmap(tmp_pixmap)

        print "... Bye"


    def set_img_2(self):
        print "Hi ..."

        fileName = "/home/ufn91840/M_Pics/kona_honzo.png"
        image = QtGui.QImage(fileName)
        tmp_pixmap = QtGui.QPixmap.fromImage(image)
        self.my_scene_2.addPixmap(tmp_pixmap)

        print "... Bye"



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())


