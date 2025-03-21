import numpy as np
from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy
from dials.algorithms.image.threshold import DispersionThresholdDebug

import pickle

class Test:
    def __init__(self):
        self.n_json_file_path = "/tmp/run_dui2_nodes/run1/imported.expt"

        experiments = ExperimentList.from_file(self.n_json_file_path)
        my_sweep = experiments.imagesets()[0]

        #print("dir(my_sweep.params)", dir(my_sweep.params), "\n")
        #print("my_sweep.params() =", my_sweep.params())

        on_sweep_img_num = 0
        self.image = my_sweep.get_raw_data(on_sweep_img_num)[0]

    def set_mask(self):
        mask_file = "/tmp/run_dui2_nodes/run2/tmp_mask.pickle"
        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()
        self.mask = mask_tup_obj[0]

    def set_pars(self):
        self.gain = 0.5
        self.size = (3, 3)
        self.nsig_b = 3
        self.nsig_s = 3
        self.global_threshold = 0
        self.min_count = 2

    def test_dispersion_debug(self):

        self.gain_map = flex.double(flex.grid(2527, 2463), self.gain)

        debug = DispersionThresholdDebug(
            self.image.as_double(),
            self.mask,
            self.gain_map,
            self.size,
            self.nsig_b,
            self.nsig_s,
            self.global_threshold,
            self.min_count,
        )

        return debug


if __name__ == "__main__":
    print("Hi")

    test1 = Test()
    test1.set_mask()
    test1.set_pars()

    a = test1.test_dispersion_debug()

    from matplotlib import pyplot as plt

    np_final_mask = a.final_mask().as_numpy_array()
    plt.imshow( np_final_mask , interpolation = "nearest" )
    plt.show()
    print(dir(a))
    np_global_mask = a.global_mask().as_numpy_array()
    plt.imshow( np_global_mask , interpolation = "nearest" )
    plt.show()


    np_cv_mask = a.cv_mask().as_numpy_array()
    plt.imshow( np_cv_mask , interpolation = "nearest" )
    plt.show()

    np_value_mask = a.value_mask().as_numpy_array()
    plt.imshow( np_value_mask , interpolation = "nearest" )
    plt.show()

    np_index_of_dispersion = a.index_of_dispersion().as_numpy_array()
    plt.imshow( np_index_of_dispersion , interpolation = "nearest" )
    plt.show()

    np_mean = a.mean().as_numpy_array()
    plt.imshow( np_mean , interpolation = "nearest" )
    plt.show()
    np_variance = a.variance().as_numpy_array()
    plt.imshow( np_variance , interpolation = "nearest" )
    plt.show()
