import subprocess
import subprocess
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
'''
from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

def run_cli_prss(cmd_to_run = None, ref_to_class = None):


    print "before subprocess"
    p = subprocess.Popen([cmd_to_run],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.STDOUT,
                            bufsize = 1)
    print "after subprocess"

    for line in iter(p.stdout.readline, b''):
        single_line = line[0:len(line)-1]
        ref_to_class.emit_print_signal(single_line)

    p.wait()
    p.stdout.close()



class MyThread (QtCore.QThread):

    str_print_signal = pyqtSignal(str)

    def __init__(self, parent = None):
        super(MyThread, self).__init__()

    def run(self):
        self.cmd_to_run = "ls -al ../"
        print "Hi from QThread(run)"
        run_cli_prss(cmd_to_run = self.cmd_to_run, ref_to_class = self)
        print "after ...close()"

    def emit_print_signal(self, str_lin):
        self.str_print_signal.emit(str_lin)


def tell_finished():
    print "tell_finished"

def cli_out(lin_str):
    print "lin_str"

'''
if __name__ == "__main__":
    thrd = MyThread()
    thrd.finished.connect(tell_finished)
    thrd.str_print_signal.connect(cli_out)
    thrd.start()
'''
