import numpy as np
from matplotlib import pyplot as plt
import pickle
import types

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy, from_numpy
from dials.algorithms.image.threshold import (
    DispersionThresholdDebug, DispersionExtendedThresholdDebug
)
from dials.command_line.find_spots import phil_scope as find_spots_phil_scope
from dials.extensions import SpotFinderThreshold



class RadialProfileThresholdDebug:
    # The radial_profile threshold algorithm does not have an associated
    # 'Debug' class. It does not create the same set of intermediate images
    # as the dispersion algorithms, so we can delegate to a
    # DispersionThresholdDebug object for those, while overriding the final_mask
    # method. This wrapper class handles that.
    def __init__(self, imageset, n_iqr, blur, n_bins):
        self.imageset = imageset
        params = find_spots_phil_scope.extract()
        params.spotfinder.threshold.radial_profile.blur = blur
        params.spotfinder.threshold.radial_profile.n_bins = n_bins
        params.spotfinder.threshold.radial_profile.n_iqr = n_iqr
        self.radial_profile = SpotFinderThreshold.load("radial_profile")(params)
        self._i_panel = 0

    def __call__(self, *args):
        dispersion = DispersionThresholdDebug(*args)
        image = args[0]
        mask = args[1]
        dispersion._final_mask = self.radial_profile.compute_threshold(
            image, mask, imageset=self.imageset, i_panel=self._i_panel
        )
        dispersion.final_mask = types.MethodType(lambda x: x._final_mask, dispersion)
        self._i_panel += 1
        return dispersion



def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def convert_2_black_n_white(np_img):
    sig_img = (np_img + 0.00000001) / np.abs(np_img + 0.00000001)
    abs_img = (sig_img + 1) / 2
    return abs_img

def from_image_n_mask_2_threshold(image, mask, imageset_tmp, pars):
    np_mask = to_numpy(mask)
    np_img = to_numpy(image)
    abs_img = convert_2_black_n_white(np_img)

    (
        nsig_b, nsig_s, global_threshold, min_count, gain, size,
        n_iqr, blur, n_bins
    ) = pars

    sum_np_mask = np_mask + abs_img - 1.5
    added_np_mask = convert_2_black_n_white(sum_np_mask)

    bool_np_mask = added_np_mask.astype(bool)
    mask_w_panels = from_numpy(bool_np_mask)

    gain_map = flex.double(flex.grid(image.all()), gain)

    my_algorithm = "radial_profile"

    if my_algorithm == "dispersion_extended":
        algorithm = DispersionExtendedThresholdDebug

    elif my_algorithm == "dispersion":
        algorithm = DispersionThresholdDebug

    else:
        algorithm = RadialProfileThresholdDebug(
            imageset_tmp, n_iqr, blur, n_bins
        )

    debug = algorithm(
        image.as_double(),
        mask_w_panels,
        gain_map, size, nsig_b, nsig_s, global_threshold, min_count,
    )

    return debug

def get_dispersion_debug_obj(
    expt_path = "/tmp/run_dui2_nodes/run1/imported.expt",
    nsig_b = 3,
    nsig_s = 3,
    global_threshold = 0,
    min_count = 2,
    gain = 1.0,
    size = (3, 3),
    n_iqr = 6,
    blur = "narrow wide",
    n_bins = 100
):
    experiments = ExperimentList.from_file(expt_path)
    my_imageset = experiments.imagesets()[0]
    on_sweep_img_num = 0
    image = my_imageset.get_raw_data(on_sweep_img_num)[0]

    try:
        mask_file = my_imageset.external_lookup.mask.filename
        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()
        mask = mask_tup_obj[0]
        print("type(mask) =", type(mask))

    except FileNotFoundError:
        mask = flex.bool(flex.grid(image.all()),True)

    pars = (
        nsig_b, nsig_s, global_threshold, min_count, gain, size,
        n_iqr, blur, n_bins
    )

    obj_w_alg = from_image_n_mask_2_threshold(image, mask, my_imageset, pars)
    return obj_w_alg


if __name__ == "__main__":
    a = get_dispersion_debug_obj(
        #expt_path = "/tmp/run_dui2_nodes/run1/imported.expt",
        #expt_path = "/tmp/run_dui2_nodes/run2/masked.expt",
        expt_path = "/tmp/run_dui2_nodes/run4/masked.expt",
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
