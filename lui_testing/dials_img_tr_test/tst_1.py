

import sys

from PyQt4 import QtCore, QtGui

class MainWidget( QtGui.QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()

        self.gridLayout = QtGui.QGridLayout(self)

        self.scrollArea_1 = QtGui.QScrollArea(self)
        self.scrollArea_1.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_1, 0, 0, 1, 1)

        self.scrollArea_2 = QtGui.QScrollArea(self)
        self.scrollArea_2.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_2, 0, 1, 1, 1)

        self.scrollArea_3 = QtGui.QScrollArea(self)
        self.scrollArea_3.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_3, 0, 2, 1, 1)

        self.scrollArea_4 = QtGui.QScrollArea(self)
        self.scrollArea_4.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_4, 2, 0, 1, 1)

        self.scrollArea_5 = QtGui.QScrollArea(self)
        self.scrollArea_5.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_5, 2, 1, 1, 1)

        self.scrollArea_6 = QtGui.QScrollArea(self)
        self.scrollArea_6.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea_6, 2, 2, 1, 1)

        self.pushButton_1 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_1, 1, 0, 1, 1)

        self.pushButton_2 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton_3 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1)

        self.pushButton_4 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)

        self.pushButton_5 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_5, 3, 1, 1, 1)

        self.pushButton_6 = QtGui.QPushButton(self)
        self.gridLayout.addWidget(self.pushButton_6, 3, 2, 1, 1)

        self.pushButton_1.clicked.connect(self.set_img)

        self.label = QtGui.QLabel()
        self.scrollArea_1.setWidget(self.label)


        self.setLayout(self.gridLayout)
        self.setWindowTitle('Testing')
        self.show()

    def set_img(self):
        print "Hi ..."
        fileName = "/home/ufn91840/M_Pics/chihuahua.png"
        #fileName = "/scratch/anaelu_git/forthon_01/miscellaneous/lena.jpeg"
        image = QtGui.QImage(fileName)

        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label.adjustSize()


        print "... Bye"

if __name__ == '__main__':
    app =  QtGui.QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())


