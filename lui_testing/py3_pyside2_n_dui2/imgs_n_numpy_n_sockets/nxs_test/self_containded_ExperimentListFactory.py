from dxtbx.model.experiment_list import ExperimentListFactory
from dxtbx.flumpy import to_numpy

from multiprocessing import Process
import os, sys, subprocess, time

def LoadImages(img_num = None):
    print("\n on_sweep_img_num =", img_num)
    experiments = get_experiments("imported.expt")
    my_sweep = experiments.imagesets()[0]
    try:
        raw_dat = my_sweep.get_raw_data(img_num)

    except RuntimeError:
        print("finished as expected after running out of images")
        return

    data_xy_flex = raw_dat[0].as_double()
    np_arr2 = to_numpy(data_xy_flex)

    txt_slice2 = str(np_arr2[50:90,40:80])
    txt_slice_tot = txt_slice2
    print(txt_slice_tot)


def get_experiments(experiment_path):
    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentListFactory.from_json_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments


def dials_import_from_path():
    try:
        path_2_import = sys.argv[1]

    except IndexError:
        print(" *** ERROR *** \n")
        print(" Must enter path to import, example: \n")
        print(" python self_containded_ExperimentListFactory_w_pyside2.py" +
              " /path/to/my/file/xx_master.h5")

        return False

    print("\n Running: \n dials.import " + path_2_import )
    subprocess.run(["dials.import", sys.argv[1]], shell=False)
    print("Done \n")
    return True


if __name__ == "__main__":
    do_the_test = dials_import_from_path()
    if do_the_test:
        for img_num in range(150):
            name = "clone # " + str(img_num)
            p = Process(target=LoadImages, args=(img_num,))
            p.start()
            p.join()
            time.sleep(0.05)

