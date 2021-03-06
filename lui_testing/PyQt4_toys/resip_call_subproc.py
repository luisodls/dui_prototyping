
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

#from cli_utils import sys_arg
import sys, os, subprocess, psutil, time

def run_my_proc(pickle_path = "", json_path = "",
                command_in = "dials.image_viewer"):

    first_pikl_path = pickle_path[0]
    obj_use_shell = True
    if(obj_use_shell == True):
        cmd_to_run = command_in + " " + str(json_path)
        if(first_pikl_path != None):
            cmd_to_run += " " + str(first_pikl_path)

    else:
        cmd_to_run = [command_in, first_pikl_path, json_path]

    cwd_path = "/tmp/dui_tst/dui_files"

    obj_phil_path = cwd_path + os.sep + "find_spots.phil"
    try:
        os.remove(obj_phil_path)

    except:
        print "no ", obj_phil_path, " found"

    print "\n running Popen>>>", cmd_to_run, ", ", obj_use_shell, "<<< \n"
    obj_my_process = subprocess.Popen(args = cmd_to_run, shell = obj_use_shell,
                                       cwd = cwd_path)

    time.sleep(0.2)
    obj_proc_pid = obj_my_process.pid
    print "obj_proc_pid =", obj_proc_pid
    time.sleep(0.2)

######################################################################################################
'''
class ExternalProcDialog(QDialog):

    read_phil_file = pyqtSignal(str)

    def __init__(self, parent = None):
        super(ExternalProcDialog, self).__init__()

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("\n          Running a pop-up viewer ...\
                               \n \
                               \n   remember to close the viewer before \
                               \n         performing any other task"))


        self.use_shell = True

        kl_but = QPushButton("Close pop-up viewer")
        kl_but.clicked.connect(self.kill_my_proc)
        vbox.addWidget(kl_but)

        self.setLayout(vbox)
        self.setModal(True)

    def run_my_proc(self, pickle_path = "", json_path = "",
                    command_in = "dials.image_viewer"):

        first_pikl_path = pickle_path[0]

        if(self.use_shell == True):
            cmd_to_run = command_in + " " + str(json_path)
            if(first_pikl_path != None):
                cmd_to_run += " " + str(first_pikl_path)

        else:
            cmd_to_run = [command_in, first_pikl_path, json_path]

        self.thrd = ViewerThread()


        cwd_path = sys_arg.directory + os.sep + "dui_files"
        self.phil_path = cwd_path + os.sep + "find_spots.phil"
        try:
            os.remove(self.phil_path)

        except:
            print "no ", self.phil_path, " found"

        print "\n running Popen>>>", cmd_to_run, ", ", self.use_shell, "<<< \n"
        self.my_process = subprocess.Popen(args = cmd_to_run, shell = self.use_shell,
                                           cwd = cwd_path)

        time.sleep(0.2)
        self.proc_pid = self.my_process.pid
        print "self.proc_pid =", self.proc_pid
        time.sleep(0.2)
        self.thrd.get_pid(self.proc_pid)

        self.thrd.finished.connect(self.child_closed)
        self.thrd.start()

        self.exec_()

    def kill_my_proc(self):
        print "self.kill_my_proc"
        self.read_phil_file.emit(self.phil_path)
        print "time to kill", self.proc_pid
        kill_w_child(self.proc_pid)
        self.done(0)


    def child_closed(self):
        print "after ...close()"
        self.kill_my_proc()

    def closeEvent(self, event):
        print "from << closeEvent  (QDialog) >>"
        self.kill_my_proc()

'''

######################################################################################################

if(__name__ == "__main__"):
    print "Hi 01"
    run_my_proc(pickle_path = ["/tmp/dui_tst/dui_files/10_experiments.json"],
                json_path = "/tmp/dui_tst/dui_files/10_reflections.pickle")
