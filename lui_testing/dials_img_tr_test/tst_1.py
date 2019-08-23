# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(748, 512)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.scrollArea_1 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName(_fromUtf8("scrollArea_1"))
        self.gridLayout.addWidget(self.scrollArea_1, 0, 0, 1, 1)

        self.scrollArea_2 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.gridLayout.addWidget(self.scrollArea_2, 0, 1, 1, 1)

        self.scrollArea_3 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName(_fromUtf8("scrollArea_3"))
        self.gridLayout.addWidget(self.scrollArea_3, 0, 2, 1, 1)

        self.scrollArea_4 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName(_fromUtf8("scrollArea_4"))
        self.gridLayout.addWidget(self.scrollArea_4, 2, 0, 1, 1)

        self.scrollArea_5 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName(_fromUtf8("scrollArea_5"))
        self.gridLayout.addWidget(self.scrollArea_5, 2, 1, 1, 1)

        self.scrollArea_6 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName(_fromUtf8("scrollArea_6"))
        self.gridLayout.addWidget(self.scrollArea_6, 2, 2, 1, 1)

        self.pushButton_1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName(_fromUtf8("pushButton_1"))
        self.gridLayout.addWidget(self.pushButton_1, 1, 0, 1, 1)

        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1)

        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)

        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout.addWidget(self.pushButton_5, 3, 1, 1, 1)

        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout.addWidget(self.pushButton_6, 3, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_1.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton", None))

        self.pushButton_1.clicked.connect(self.set_img)


    def set_img(self):
        print "Hi ..."
        fileName = "../../../anaelu_git/forthon_01/miscellaneous/lena.jpeg"
        image = QtGui.QImage(fileName)
        self.label = QtGui.QLabel()
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scrollArea_1.setWidget(self.label)
        print "... Bye"


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

