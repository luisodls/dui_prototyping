import subprocess

from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

class CommandThread(QtCore.QThread):

    str_print_signal = QtCore.Signal(str)
    str_fail_signal = QtCore.Signal()

    def __init__(self, parent=None):
        super(CommandThread, self).__init__()

    def __call__(self, cmd_to_run, ref_to_controler):
        self.cmd_to_run = cmd_to_run
        self.ref_to_controler = ref_to_controler
        self.status_thread = CheckStatusThread()
        self.status_thread(self.ref_to_controler)
        self.start()

    def run(self):
        print("self.cmd_to_run =", self.cmd_to_run)
        self.ref_to_controler.run(command=self.cmd_to_run, ref_to_class=self)

    def emit_print_signal(self, str_lin):
        print(str_lin, ":<<")
        self.str_print_signal.emit(str_lin)

    def emit_fail_signal(self):
        #self.str_fail_signal.emit()
        print("emit_fail_signal")


class run_cmd(object):
    def __init__(self, cmd2run):
        self.cmd_thread = CommandThread()
        print("\nRunning:", cmd2run, "\n")

        my_process = subprocess.Popen(
            cmd2run,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
        )

        for line in iter(my_process.stdout.readline, b""):
            single_line = line[0 : len(line) - 1]
            print(">>: ", single_line)
            self.cmd_thread.emit_print_signal(str_lin = single_line)

        my_process.wait()
        my_process.stdout.close()

        print(cmd2run, "finished")


if __name__ == "__main__":
    run_cmd("ls -al ../")
    run_cmd("dials.import ")

