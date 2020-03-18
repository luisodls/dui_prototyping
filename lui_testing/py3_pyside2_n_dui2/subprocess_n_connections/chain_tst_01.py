import subprocess
import os

def run_cmd(cmd_to_run):
    proc = subprocess.Popen(
        cmd_to_run,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    line = None
    while proc.poll() is None or line != '':
        line = proc.stdout.readline()[:-1]
        print("line>>", line)
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
        "dials.index",
        "dials.refine",
        ]

    old_dir = "/tmp/dui2run/run_zero"
    for num, comd in enumerate(cmd_lst):
        print("\n num=", num, "comd", comd)
        new_dir = "run" + str(num)
        os.mkdir(new_dir)
        os.chdir(new_dir)

        new_cmd = comd + " " + old_dir + "/*.expt " + old_dir + "/*.refl "

        print("\n new_cmd ", new_cmd)

        run_cmd(comd)
        old_dir = os.getcwd()
        os.chdir("..")


    '''
    path = "/tmp/home/monthly/daily/hourly"
    os.mkdir( path, 0755 )

    os.chdir(path)

    os.getcwd()

    run_cmd("")

>>> os.mkdir("x")
>>> os.chdir("x")
>>> os.getcwd()
    '''


