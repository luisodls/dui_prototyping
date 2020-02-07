import subprocess
import subprocess
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
'''
from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

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

class MyThread (QtCore.QThread):

    str_print_signal = QtCore.Signal(str)

    def __init__(self, parent = None):
        super(MyThread, self).__init__()


    def run(self):
        self.cmd_to_run = "dials.import"
        print("Hi from QThread(run)")
        run_cli_prss(cmd_to_run = self.cmd_to_run, ref_to_class = self)
        print("after ...close()")

    def emit_print_signal(self, str_lin):
        self.str_print_signal.emit(str_lin)


if __name__ == "__main__":
    bkp = '''
    self.thrd = MyThread()
    self.thrd.finished.connect(self.tell_finished)
    self.thrd.str_print_signal.connect(self.cli_out)
    self.pushbutton.clicked.connect(self.thrd.start)
    '''

