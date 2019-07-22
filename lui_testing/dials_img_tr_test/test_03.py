from __future__ import absolute_import, division, print_function

from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory
import pickle

class Test:
    def __init__(self):
        from scitbx.array_family import flex

        # Create an image
        self.image = flex.random_double(2527 * 2463, 10)
        self.image.reshape(flex.grid(2527, 2463))
        self.mask = flex.random_bool(2527 * 2463, 0.99)
        self.mask.reshape(flex.grid(2527, 2463))
        self.gain = flex.random_double(2527 * 2463) + 0.5
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

        imageset_tmp = experiments.imagesets()[0]
        mask_file = imageset_tmp.external_lookup.mask.filename

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
        result = debug.final_mask()
        return result


if __name__ == "__main__":
    print("Hi")

    test1 = Test()
    test1.set_img()
    test1.set_mask()

    a = test1.test_dispersion_debug()

    np_alg = a.as_numpy_array()

    from matplotlib import pyplot as plt
    plt.imshow( np_alg , interpolation = "nearest" )
    plt.show()
