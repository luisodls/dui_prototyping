from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton, QStyle, QWidget)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        layout = QGridLayout()
        btn = QPushButton("click me")
        btn.clicked.connect(self.clicked_me)
        layout.addWidget(btn)
        self.setLayout(layout)

    def clicked_me(self):
        print("clicked me")

def main():
    app = QApplication([])
    w = Window()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
