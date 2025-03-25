import numpy as np
from matplotlib import pyplot as plt
import pickle

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy, from_numpy
from dials.algorithms.image.threshold import (
    DispersionThresholdDebug, DispersionExtendedThresholdDebug
)


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

    abs_img = convert_2_black_n_white(np_img)
    #draw_pyplot(abs_img)

    try:
        mask_file = my_sweep.external_lookup.mask.filename
        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()
        mask = mask_tup_obj[0]
        print("type(mask) =", type(mask))

    except FileNotFoundError:
        mask = flex.bool(flex.grid(image.all()),True)

    np_mask = to_numpy(mask)
    sum_np_mask = np_mask + abs_img - 1.5
    #draw_pyplot(sum_np_mask)
    added_np_mask = convert_2_black_n_white(sum_np_mask)
    #draw_pyplot(added_np_mask)

    bool_np_mask = added_np_mask.astype(bool)
    mask = from_numpy(bool_np_mask)

    #print("type(mask) =", type(mask))
    #print("self.image.all() =", image.all())

    gain_map = flex.double(flex.grid(image.all()), gain)

    my_algorithm = "dispersion_extended"

    if my_algorithm == "dispersion_extended":
        algorithm = DispersionExtendedThresholdDebug
    elif my_algorithm == "dispersion":
        algorithm = DispersionThresholdDebug
    to_view_later = '''
    else:
        algorithm = RadialProfileThresholdDebug(
            image, self.settings.n_iqr, self.settings.blur, self.settings.n_bins
        )

    radial_profile {
      n_iqr = 6
      blur = narrow wide
      n_bins = 100
    '''


    debug = algorithm(
        image.as_double(),
        mask, gain_map, size, nsig_b, nsig_s, global_threshold, min_count,
    )

    return debug


if __name__ == "__main__":
    a = get_dispersion_debug_obj(
        #expt_path = "/tmp/run_dui2_nodes/run1/imported.expt",
        expt_path = "/tmp/run_dui2_nodes/run2/masked.expt",
        #expt_path = "/scratch/30day_tmp/run_dui2_nodes/run2/masked.expt",
        nsig_b = 3,
        nsig_s = 3,
        global_threshold = 0,
        min_count = 2,
        gain = 1.0,
        size = (3, 3),
    )

    print("a.final_mask ... threshold")
    draw_pyplot(to_numpy(a.final_mask()))

    print("global_mask ... global")
    draw_pyplot(to_numpy(a.global_mask()))

    print("cv_mask  ... sigma_b")
    draw_pyplot(to_numpy(a.cv_mask()))

    print("value_mask ... sigma_s")
    draw_pyplot(to_numpy(a.value_mask()))

    print("index_of_dispersion ... dispersion")
    draw_pyplot(to_numpy(a.index_of_dispersion()))

    print("mean ... mean")
    draw_pyplot(to_numpy(a.mean()))

    print("variance ... variance")
    draw_pyplot(to_numpy(a.variance()))
