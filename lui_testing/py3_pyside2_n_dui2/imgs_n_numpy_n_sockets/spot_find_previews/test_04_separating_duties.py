import numpy as np
from matplotlib import pyplot as plt

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy
from dials.algorithms.image.threshold import DispersionThresholdDebug

import pickle

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def get_dispersion_debug_obj(expt_path):
    experiments = ExperimentList.from_file(expt_path)
    my_sweep = experiments.imagesets()[0]

    on_sweep_img_num = 0
    image = my_sweep.get_raw_data(on_sweep_img_num)[0]

    try:
        mask_file = my_sweep.external_lookup.mask.filename
        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()
        mask = mask_tup_obj[0]
        print("type(mask) =", type(mask))

    except FileNotFoundError:
        mask = flex.bool(flex.grid(image.all()),True)

    nsig_b = 3
    nsig_s = 3
    global_threshold = 0
    min_count = 2
    gain = 1.0
    size = (3, 3)

    print("self.image.all() =", image.all())

    gain_map = flex.double(flex.grid(image.all()), gain)
    debug = DispersionThresholdDebug(
        image.as_double(),
        mask, gain_map, size, nsig_b, nsig_s, global_threshold, min_count,
    )

    return debug


if __name__ == "__main__":
    print("Hi")

    a = get_dispersion_debug_obj("/tmp/run_dui2_nodes/run1/imported.expt")
    #a = get_dispersion_debug_obj("/scratch/30day_tmp/run_dui2_nodes/run2/masked.expt")
    #a = get_dispersion_debug_obj("/tmp/run_dui2_nodes/run2/masked.expt")

    print("final_mask")
    draw_pyplot(a.final_mask().as_numpy_array())

    print("global_mask")
    draw_pyplot(a.global_mask().as_numpy_array())

    print("cv_mask")
    draw_pyplot(a.cv_mask().as_numpy_array())

    print("value_mask")
    draw_pyplot(a.value_mask().as_numpy_array())

    print("index_of_dispersion")
    draw_pyplot(a.index_of_dispersion().as_numpy_array())

    print("mean")
    draw_pyplot(a.mean().as_numpy_array())

    print("variance")
    draw_pyplot(a.variance().as_numpy_array())





