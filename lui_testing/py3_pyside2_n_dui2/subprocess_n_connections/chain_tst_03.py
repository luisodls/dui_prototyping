import subprocess
import os
import glob

class node(object):
    def __init__(self, old_node = None):
        self._old_node = old_node
        self._lst_expt = []
        self._lst_refl = []
        self._lst2run = []
        self._run_dir = ""

        try:
            print("old_node.dir =", self._old_node._run_dir)
            self._lst_expt = glob.glob(self._old_node._run_dir + "/*.expt")
            self._lst_refl = glob.glob(self._old_node._run_dir + "/*.refl")

            if len(self._lst_expt) == 0:
                self._lst_expt = self._old_node._lst_expt

            if len(self._lst_refl) == 0:
                self._lst_refl = self._old_node._lst_refl

            print("self._lst_expt: ", self._lst_expt)
            print("self._lst_refl: ", self._lst_refl)

        except:
            print("NOT _run_dir on old_node")


    def set_cmd_lst(self, lst_in):
        self._lst2run = [lst_in[0]]
        self.set_imp_fil(self._lst_expt, self._lst_refl)
        try:
            for par in lst_in[1:]:
                self._lst2run.append(par)

        except:
            print("no extra parameters")

    def set_run_dir(self, dir_in):
        self._run_dir = dir_in

    def set_imp_fil(self, lst_expt, lst_refl):
        for expt_2_add in lst_expt:
            self._lst2run.append(expt_2_add)

        for refl_2_add in lst_refl:
            self._lst2run.append(refl_2_add)

    def run_cmd(self):

        print("self._lst2run:", self._lst2run)
        print("self._run_dir:", self._run_dir)

        proc = subprocess.Popen(
            self._lst2run,
            shell=False,
            cwd=self._run_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        line = None
        while proc.poll() is None or line != '':
            line = proc.stdout.readline()[:-1]
            print("Out>> ", line)
            '''
            line_err = proc.stderr.readline()[:-1]
            if line_err != '':
                print("_err>>", line_err)
            '''

        proc.stdout.close()


if __name__ == "__main__":

    cmd_lst = [
        ["dials.find_spots", "nproc=5"],
        ["dials.index"],
        ["dials.refine"],
        ["dials.integrate", "nproc=5"],
        ["dials.scale"],
        ]

    old_node = node(None)
    old_node.set_run_dir("/tmp/dui2run/tst_chain/imp_dir")
    old_node._lst_expt = ["/tmp/dui2run/tst_chain/imp_dir/imported.expt"]
    old_node._lst_refl = []
    base_dir = os.getcwd()

    for num, comd in enumerate(cmd_lst):
        print("\n num=", num, "comd", comd, "\n")
        new_dir = base_dir + "/run" + str(num)
        print("new_dir: ", new_dir, "\n")
        os.mkdir(new_dir)

        new_node = node(old_node)
        new_node.set_run_dir(new_dir)
        new_node.set_cmd_lst(comd)
        new_node.run_cmd()

        old_node = new_node



