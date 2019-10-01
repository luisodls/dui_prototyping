'''
import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *
'''

import PySide2
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWebKitWidgets import QWebView , QWebPage
from PySide2.QtWebKit import QWebSettings
from PySide2.QtNetwork import *
'''
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWebKit import *
'''

import sys
from optparse import OptionParser

class Browser(QWebView):
    def __init__(self):
        self.view = QWebView.__init__(self)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)

    def load(self,url):
        self.setUrl(QUrl(url))

    def adjustTitle(self):
        self.setWindowTitle(self.title())

    def disableJS(self):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)



app = QApplication(sys.argv)
view = Browser()
view.showMaximized()
#view.load("https://uglymol.github.io/reciprocal.html?rlp=data/rlp.csv")
view.load("https://google.com")

app.exec_()
