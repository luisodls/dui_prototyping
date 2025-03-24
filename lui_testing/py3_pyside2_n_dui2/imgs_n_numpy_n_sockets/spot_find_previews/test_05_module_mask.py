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

def convert_2_black_n_white(np_img):
    sig_img = (np_img + 0.00000001) / np.abs(np_img + 0.00000001)
    abs_img = (sig_img + 1) / 2
    return abs_img

def get_dispersion_debug_obj(
    expt_path = "/tmp/run_dui2_nodes/run1/imported.expt",
    nsig_b = 3,
    nsig_s = 3,
    global_threshold = 0,
    min_count = 2,
    gain = 1.0,
    size = (3, 3),
):
    experiments = ExperimentList.from_file(expt_path)
    my_sweep = experiments.imagesets()[0]

    on_sweep_img_num = 0
    image = my_sweep.get_raw_data(on_sweep_img_num)[0]

    np_img = to_numpy(image)
    '''
    sig_img = (np_img + 0.00000001) / np.abs(np_img + 0.00000001)
    abs_img = (sig_img + 1) / 2
    '''
    abs_img = convert_2_black_n_white(np_img)
    draw_pyplot(abs_img)

    try:
        mask_file = my_sweep.external_lookup.mask.filename
        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()
        mask = mask_tup_obj[0]

        np_mask = to_numpy(mask)

        sum_np_mask = np_mask + abs_img + 1

        draw_pyplot(convert_2_black_n_white(sum_np_mask))
        draw_pyplot(sum_np_mask)

        draw_pyplot(to_numpy(mask))

        print("type(mask) =", type(mask))

    except FileNotFoundError:
        mask = flex.bool(flex.grid(image.all()),True)

    print("self.image.all() =", image.all())

    gain_map = flex.double(flex.grid(image.all()), gain)
    debug = DispersionThresholdDebug(
        image.as_double(),
        mask, gain_map, size, nsig_b, nsig_s, global_threshold, min_count,
    )

    return debug


if __name__ == "__main__":
    print("Hi")

    a = get_dispersion_debug_obj(
        #expt_path = "/tmp/run_dui2_nodes/run1/imported.expt",
        #expt_path = "/scratch/30day_tmp/run_dui2_nodes/run2/masked.expt",
        expt_path = "/tmp/run_dui2_nodes/run2/masked.expt",
        nsig_b = 3,
        nsig_s = 3,
        global_threshold = 0,
        min_count = 2,
        gain = 1.0,
        size = (3, 3),
    )

    print("final_mask")
    draw_pyplot(to_numpy(a.final_mask()))
    '''

    print("global_mask")
    draw_pyplot(to_numpy(a.global_mask()))

    print("cv_mask")
    draw_pyplot(to_numpy(a.cv_mask()))

    print("value_mask")
    draw_pyplot(to_numpy(a.value_mask()))

    print("index_of_dispersion")
    draw_pyplot(to_numpy(a.index_of_dispersion()))

    print("mean")
    draw_pyplot(to_numpy(a.mean()))

    print("variance")
    draw_pyplot(to_numpy(a.variance()))
    '''
