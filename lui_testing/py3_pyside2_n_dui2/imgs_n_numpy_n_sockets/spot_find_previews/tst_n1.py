import numpy as np
from matplotlib import pyplot as plt

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()


def get_np_full_img(raw_dat):
    print("Using the first panel only")
    data_xy_flex = raw_dat[0].as_double()
    np_arr = to_numpy(data_xy_flex)

    print("type(np_arr[0,0]) = " + str(type(np_arr[0,0])))

    return np_arr


if __name__ == "__main__":
    exp_path = "/tmp/run_dui2_nodes/run1/imported.expt"
    experiments = ExperimentList.from_file(exp_path)
    my_sweep = experiments.imagesets()[0]

    print("dir(my_sweep.params)", dir(my_sweep.params), "\n")
    print("my_sweep.params() =", my_sweep.params())

    on_sweep_img_num = 0
    raw_dat = my_sweep.get_raw_data(on_sweep_img_num)

    np_arr = get_np_full_img(raw_dat)

    draw_pyplot(np_arr)

    print("type(np_arr) = ", type(np_arr))
