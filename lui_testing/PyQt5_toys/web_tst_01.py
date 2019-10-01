
#from PyQt4 import QtCore, QtGui, QtWebKit
from PySide2 import QtCore, QtGui,  QtWebEngineWidgets, QtWidgets
# QtWebKit,
import sys


#            from PySide2.QtGui import *
#            from PySide2.QtCore import *
#            from PySide2.QtWidgets import *


class ImgTab( QtWidgets.QWidget):

    def __init__(self):
        super(ImgTab, self).__init__()

        QtWebEngineWidgets.JavascriptEnabled = True
        #.QWebSettings

        self.web = QtWebEngineWidgets.QWebEngineView()
        #print "dir(self.web) =", dir(self.web)


        self.web.load(QtCore.QUrl("https://au.yahoo.com"))
        #self.web.load(QtCore.QUrl("file:///tmp/ ... /dials-report.html"))

        hbox =  QtWidgets.QHBoxLayout()
        hbox.addWidget(self.web)

        #self.setGeometry(1100, 200, 550, 250)
        self.setLayout(hbox)
        self.setWindowTitle('Shell dialog')
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ImgTab()
    sys.exit(app.exec_())
