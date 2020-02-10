import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import time
import subprocess

def run_cli_prss(cmd_to_run = None, ref_to_class = None):
    proc = subprocess.Popen(cmd_to_run,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    line = None
    while proc.poll() is None or line != '':
        line = proc.stdout.readline()[:-1]
        ref_to_class.emit_print_signal(line)

    #proc.wait()
    proc.stdout.close()

class MyThread (QThread):

    str_print_signal = Signal(str)

    def __init__(self, parent = None):
        super(MyThread, self).__init__()

    def run(self):
        self.cmd_to_run = "dials.import"
        print(" Hi from QThread(run) \n")
        run_cli_prss(cmd_to_run = self.cmd_to_run, ref_to_class = self)
        print("\n after ...close()")

    def emit_print_signal(self, str_lin):
        self.str_print_signal.emit(str_lin)

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Qthread Toy')

        self.thrd = MyThread()
        self.thrd.finished.connect(self.tell_finished)
        main_box = QHBoxLayout()

        self.thrd.str_print_signal.connect(self.cli_out)

        self.textedit = QTextEdit()
        main_box.addWidget(self.textedit)

        self.pushbutton = QPushButton('Click Me')
        main_box.addWidget(self.pushbutton)
        self.pushbutton.clicked.connect(self.thrd.start)

        self.setLayout(main_box)
        self.show()

    def tell_finished(self):
        print("finished thread")

    def cli_out(self, lin_to_prn):
        #print lin_to_prn, " <<"
        self.textedit.append(lin_to_prn)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

