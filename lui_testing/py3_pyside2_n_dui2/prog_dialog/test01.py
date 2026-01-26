import sys, os, platform

try:
    from PySide6.QtWebEngineCore import QWebEngineSettings
    from PySide6 import QtUiTools
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    print("Using PySide6 as Qt bindings")

except ModuleNotFoundError:
    from PySide2 import QtUiTools
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    print("Using PySide2 as Qt bindings")


class Progress_Box(QDialog):
    def __init__(self, parent = None):
        super(Progress_Box, self).__init__(parent)

        Stop_Butn = QPushButton("Stop ...")
        Stop_Butn.clicked.connect(self.stop_me)

        self.live_label = QLabel("progress")
        self.num_in_label = 0

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.live_label)
        mainLayout.addWidget(Stop_Butn)
        self.setLayout(mainLayout)
        self.setWindowTitle("Loading")

        timer = QTimer(self)
        timer.timeout.connect(self.update_me)
        timer.start(500)

    def stop_me(self):
        print("time to stop")

    def update_me(self):
        self.num_in_label += 5
        self.live_label.setText(str(self.num_in_label))

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.window.Button1.clicked.connect(self.clicked)

        main_box = QVBoxLayout()
        main_box.addWidget(QLabel("Testing"))

        self.p_box = Progress_Box()

        self.window.InerWidget.setLayout(main_box)
        self.window.show()

    def clicked(self):
        print("clicked")
        self.p_box.show()


if __name__ == '__main__':
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
    print("platform.system()" + str(platform.system()))
    if platform.system() == "Windows":
        win_str = "true"

    else:
        #TODO: test this variables on m1 mac
        win_str = "false"
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        os.environ["WAYLAND_DISPLAY"] = ""

    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())
