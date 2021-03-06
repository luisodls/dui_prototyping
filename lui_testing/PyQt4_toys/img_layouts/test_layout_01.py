
from PySide import QtCore, QtGui


class ImgWidg(QtGui.QWidget):
    def __init__(self, parent = None, img_path = None):
        super(ImgWidg, self).__init__()

        self.imageLabel = QtGui.QLabel()
        self.image = QtGui.QImage(img_path)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))

        bg_box =  QtGui.QVBoxLayout(self)
        bg_box.addWidget(self.imageLabel)

        self.setLayout(bg_box)
        self.show()


class MyScroll(QtGui.QScrollArea):

    def __init__(self, parent = None):
        super(MyScroll, self).__init__()

        self.imageWidg = ImgWidg(self, "centroid_diff_z.png")
        self.setWidget(self.imageWidg)
        self.show()

    def update_me(self, img_list = None):
        print "update_me(self)"
        self.imageLabel = QtGui.QLabel()
        self.image = QtGui.QImage("centroid_rmsd_vs_phi.png")
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.setWidget(self.imageLabel)
        self.show()


class ImgTab(QtGui.QWidget):

    def __init__(self, parent = None):
        super(ImgTab, self).__init__()

        self.scrollArea = MyScroll(self)
        main_box = QtGui.QVBoxLayout()
        self.btn_go = QtGui.QPushButton('\n      Go   \n', self)
        self.btn_go.clicked.connect(self.B_go_clicked)

        main_box.addWidget(self.btn_go)
        main_box.addWidget(self.scrollArea)

        self.setLayout(main_box)
        self.show()

    def B_go_clicked(self):
        print "B_go_clicked(self)"
        self.scrollArea.update_me()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    frame = ImgTab()
    sys.exit(app.exec_())
