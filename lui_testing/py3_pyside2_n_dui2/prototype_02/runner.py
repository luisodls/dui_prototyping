from PySide2 import QtCore
import subprocess

class MyThread (QtCore.QThread):

    str_print_signal = QtCore.Signal(str)

    def __init__(self, parent = None):
        super(MyThread, self).__init__()

    def set_cmd(self, cmd_in = None):
        self.cmd_to_run = cmd_in

    def run(self):
        print("... from QThread(run)")

        proc = subprocess.Popen(
            self.cmd_to_run,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        line = None
        while proc.poll() is None or line != '':
            line = proc.stdout.readline()[:-1]
            self.emit_print_signal(line)

        proc.stdout.close()

        print("after proc.stdout.close() ...")

    def emit_print_signal(self, str_lin):
        self.str_print_signal.emit(str_lin)



