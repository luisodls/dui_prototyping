from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import os, sys

class Button(QToolButton):
    usr_click = Signal()
    def __init__(self):
        super().__init__()
        self.icon_path_n = "icon_resources" + os.sep + "new_layout.png"
        self.icon_path_cl = "icon_resources" + os.sep + "new_layout_clear.png"
        self.txt_n = "aaaaaa \n bbbbbbbb"
        self.txt_cl = "      ...     \n       "
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setText(self.txt_n)
        self.setIcon(QIcon(self.icon_path_cl))
        self.setIconSize(QSize(38, 42))
        self.setAutoRaise(True)

        self.clicked.connect(self.emmit_click)

    def enterEvent(self, event):
        self.setIcon(QIcon(self.icon_path_n))
        self.setText(self.txt_n)

    def leaveEvent(self, event):
        self.setIcon(QIcon(self.icon_path_cl))
        self.setText(self.txt_cl)

    def emmit_click(self):
        self.usr_click.emit()

class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "simple.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI Cloud")
        self.window.GrayButton.clicked.connect(self.gray_but)
        self.window.pushButton.clicked.connect(self.but_clic)
        self.enable_state = True

        nxt_butt = Button()
        nxt_butt.usr_click. connect(self.tool_butt_click)

        self.window.TstVerticalLayout.addWidget(nxt_butt)
        self.window.show()

    def gray_but(self):
        print("GrayButton clicked")
        self.enable_state = not self.enable_state
        self.window.pushButton.setEnabled(self.enable_state)

    def but_clic(self):
        print("pushButton clicked")

    def tool_butt_click(self):
        print("tool_butt_click")


if __name__ == "__main__":
    script = os.path.realpath(__file__)
    print("SCript path:", script)
    print("__file__:", __file__)
    print("SCript DIR path:", os.path.realpath(__file__)[0:-len(str(__file__))])

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    m_obj = MainObject()
    sys.exit(app.exec_())
