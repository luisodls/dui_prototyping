import subprocess
import os
import glob

class node(object):
    def __init__(self):
        self.old_lst_expt = []
        self.old_lst_refl = []

    def set_cmd_lst(self, lst_in):
        self._lst2run = lst_in

    def run_cmd(self):
        proc = subprocess.Popen(
            self._lst2run,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        line = None
        while proc.poll() is None or line != '':
            line = proc.stdout.readline()[:-1]
            print("out_lin>>", line)
            '''
            line_err = proc.stderr.readline()[:-1]
            if line_err != '':
                print("_err>>", line_err)
            '''

        proc.stdout.close()


if __name__ == "__main__":

    to_add_later = [
        "dials.import /tmp/dui2run/imgs/X4_wide_M1S4_2_00*.cbf image_range=1,12",
        "dials.find_spots  ../tst1/*.expt ../tst1/*.refl spotfinder.threshold.dispersion.gain=1.1",

        "dials.integrate ../tst4/*.expt ../tst4/*.refl integration.mp.nproc=4",
        "dials.scale ../tst5/*.expt ../tst5/*.refl",
        "dials.symmetry ../tst6/*.expt ../tst6/*.refl",
        ]

    cmd_lst = [
        "dials.find_spots",
        "dials.index",
        "dials.refine",
        "dials.integrate",
        "dials.scale",
        ]

    #old_dir = "/tmp/dui2run/tst_chain/run_zero"

    old_dir = "/tmp/dui2run/tst_chain/imp_dir"

    old_lst_expt = ["/tmp/dui2run/tst_chain/imp_dir/imported.expt"]
    old_lst_refl = []

    for num, comd in enumerate(cmd_lst):
        print("\n num=", num, "comd", comd)
        new_dir = "run" + str(num)
        os.mkdir(new_dir)
        os.chdir(new_dir)

        lst_expt = glob.glob(old_dir + "/*.expt")
        lst_refl = glob.glob(old_dir + "/*.refl")

        print("lst_expt: ", lst_expt)
        print("lst_refl: ", lst_refl)

        if len(lst_expt) == 0:
            lst_expt = old_lst_expt

        if len(lst_refl) == 0:
            lst_refl = old_lst_refl

        new_cmd = str(comd)

        for expt_2_add in lst_expt:
            new_cmd += " " + expt_2_add

        for refl_2_add in lst_refl:
            new_cmd += " " + refl_2_add

        print("\n new_cmd ", new_cmd)

        new_node = node()
        new_node.set_cmd_lst(new_cmd)
        new_node.run_cmd()

        #run_cmd(new_cmd)

        old_dir = os.getcwd()
        old_lst_expt = lst_expt
        old_lst_refl = lst_refl

        os.chdir("..")



