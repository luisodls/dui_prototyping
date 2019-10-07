
#from PyQt4 import QtCore, QtGui, QtWebKit
#from PySide2 import QtCore, QtGui,  QtWebEngineWidgets, QtWidgets

import sys

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtWebKit import *



class ImgTab( QWidget):

    def __init__(self):
        super(ImgTab, self).__init__()

        #settings = QWebSettings.globalSettings()
        #settings.setAttribute(QWebSettings.JavascriptEnabled, False)

        self.web = QWebView()
        #print "dir(self.web) =", dir(self.web)


        self.web.load(QUrl("https://au.yahoo.com"))
        #self.web.load(QtCore.QUrl("file:///tmp/ ... /dials-report.html"))

        hbox =  QHBoxLayout()
        hbox.addWidget(self.web)

        #self.setGeometry(1100, 200, 550, 250)
        self.setLayout(hbox)
        self.setWindowTitle('Shell dialog')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImgTab()
    sys.exit(app.exec_())
