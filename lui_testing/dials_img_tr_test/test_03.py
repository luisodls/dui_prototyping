from __future__ import absolute_import, division, print_function

from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory
from scitbx.array_family import flex

import pickle

class Test:
    def __init__(self):


        # Create an image
        self.image = flex.random_double(2527 * 2463, 10)
        self.image.reshape(flex.grid(2527, 2463))
        self.mask = flex.random_bool(2527 * 2463, 0.99)
        self.mask.reshape(flex.grid(2527, 2463))
        #self.gain = flex.double(2527 * 2463) + 0.5
        self.gain = flex.double(2527 * 2463) + 5.5
        self.gain.reshape(flex.grid(2527, 2463))
        self.size = (3, 3)
        self.min_count = 2


    def set_img(self):
        self.n_json_file_path = "/tmp/dui_run/dui_files/2_datablock.json"
        datablocks = DataBlockFactory.from_json_file(self.n_json_file_path)
        # TODO check length of datablock for safety
        datablock = datablocks[0]
        my_sweep = datablock.extract_sweeps()[0]
        self.image = my_sweep.get_raw_data(0)[0].as_double()

    def set_mask(self):
        experiments = ExperimentListFactory.from_json_file(
                        self.n_json_file_path, check_format=False
                    )

        self.imageset = experiments.imagesets()[0]
        mask_file = self.imageset.external_lookup.mask.filename

        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()

        self.mask = mask_tup_obj[0]


    def test_dispersion_debug(self):
        from dials.algorithms.image.threshold import DispersionThresholdDebug

        nsig_b = 3
        nsig_s = 3

        debug = DispersionThresholdDebug(
            self.image,
            self.mask,
            self.gain,
            self.size,
            nsig_b,
            nsig_s,
            0,
            self.min_count,
        )


        return debug


if __name__ == "__main__":
    print("Hi")

    test1 = Test()
    test1.set_img()
    test1.set_mask()

    a = test1.test_dispersion_debug()

    #print("dir(debug)", dir(debug))

    '''
    'cv_mask', 'final_mask', 'global_mask',
    'index_of_dispersion', 'mean',
    'value_mask', 'variance'
    '''

    from matplotlib import pyplot as plt

    np_final_mask = a.final_mask().as_numpy_array()
    plt.imshow( np_final_mask , interpolation = "nearest" )
    plt.show()

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

