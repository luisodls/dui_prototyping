import numpy as np
from matplotlib import pyplot as plt
import pickle
import types
import time

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy, from_numpy
from dials.algorithms.image.threshold import (
    DispersionThresholdDebug, DispersionExtendedThresholdDebug
)
from dials.command_line.find_spots import phil_scope as find_spots_phil_scope
from dials.extensions import SpotFinderThreshold


def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()


################################          no need to copy/paste start

def get_correct_img_num_n_sweep_num(experiments, img_num):

    # no need to copy/paste this function

    lst_num_of_imgs = []
    for single_sweep in experiments.imagesets():
        lst_num_of_imgs.append(len(single_sweep.indices()))

    on_sweep_img_num = img_num
    n_sweep = 0
    for num_of_imgs in lst_num_of_imgs:
        if on_sweep_img_num >= num_of_imgs:
            on_sweep_img_num -= num_of_imgs
            n_sweep += 1

        else:
            break

    return on_sweep_img_num, n_sweep

def get_experiments(experiment_path):

    # no need to copy/paste this function

    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentList.from_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments

def get_np_full_mask_from_i23_raw(tuple_of_flex_mask):

    # no need to copy/paste this function

    pan_tup = tuple(range(24))
    np_top_pan = to_numpy(tuple_of_flex_mask[pan_tup[0]])
    p_siz0 = np.size(np_top_pan[:, 0:1])
    p_siz1 = np.size(np_top_pan[0:1, :])
    p_siz_bg = p_siz0 + 18

    im_siz0 = p_siz_bg * len(pan_tup)
    im_siz1 = p_siz1

    np_arr = np.zeros((im_siz0, im_siz1), dtype=bool)
    np_arr[:, :] = 1
    np_arr[0:p_siz0, 0:p_siz1] = np_top_pan[:, :]

    for s_num in pan_tup[1:]:
        pan_dat = to_numpy(tuple_of_flex_mask[pan_tup[s_num]])
        np_arr[
            s_num * p_siz_bg : s_num * p_siz_bg + p_siz0, 0:p_siz1
        ] = pan_dat[:, :]

    return np_arr

################################          no need to copy/paste end


class RadialProfileThresholdDebug:
    # The radial_profile threshold algorithm does not have an associated
    # 'Debug' class. It does not create the same set of intermediate images
    # as the dispersion algorithms, so we can delegate to a
    # DispersionThresholdDebug object for those, while overriding the final_mask
    # method. This wrapper class handles that.

    # This class was Copy/Pasted and edited from the module spotfinder_frame.py
    # that is par of the Dials image viewer

    def __init__(self, imageset, n_iqr, blur, n_bins):
        self.imageset = imageset
        params = find_spots_phil_scope.extract()
        params.spotfinder.threshold.radial_profile.blur = blur
        params.spotfinder.threshold.radial_profile.n_bins = n_bins
        params.spotfinder.threshold.radial_profile.n_iqr = n_iqr
        self.radial_profile = SpotFinderThreshold.load("radial_profile")(params)
        self.i_panel = 0

    def __call__(self, *args):
        dispersion = DispersionThresholdDebug(*args)
        image = args[0]
        mask = args[1]
        dispersion._final_mask = self.radial_profile.compute_threshold(
            image, mask, imageset=self.imageset, i_panel=self.i_panel
        )
        dispersion.final_mask = types.MethodType(lambda x: x._final_mask, dispersion)
        return dispersion


def convert_2_black_n_white(np_img):
    sig_img = (np_img + 0.00000001) / np.abs(np_img + 0.00000001)
    abs_img = (sig_img + 1) / 2
    return abs_img


def from_image_n_mask_2_threshold(
    flex_image, mask, imageset_tmp, pars, panel_number
):
    np_mask = to_numpy(mask)
    np_img = to_numpy(flex_image)
    abs_img = convert_2_black_n_white(np_img)

    (
        nsig_b, nsig_s, global_threshold, min_count, gain, size,
        n_iqr, blur, n_bins
    ) = pars

    sum_np_mask = np_mask + abs_img - 1.5
    added_np_mask = convert_2_black_n_white(sum_np_mask)

    bool_np_mask = added_np_mask.astype(bool)
    mask_w_panels = from_numpy(bool_np_mask)

    gain_map = flex.double(flex.grid(flex_image.all()), gain)

    my_algorithm = "radial_profile"
    #my_algorithm = "dispersion"
    #my_algorithm = "dispersion_extended"

    if my_algorithm == "dispersion_extended":
        algorithm = DispersionExtendedThresholdDebug

    elif my_algorithm == "dispersion":
        algorithm = DispersionThresholdDebug

    else:
        algorithm = RadialProfileThresholdDebug(
            imageset_tmp, n_iqr, blur, n_bins
        )
    algorithm.i_panel = panel_number
    debug = algorithm(
        flex_image.as_double(),
        mask_w_panels,
        gain_map, size, nsig_b, nsig_s, global_threshold, min_count,
    )
    return debug

def get_dispersion_debug_obj_tup(
    expt_path = "/tmp/...", on_sweep_img_num = 0, params_in = {None}
):

    nsig_b =            params_in["nsig_b"]
    nsig_s =            params_in["nsig_s"]
    global_threshold =  params_in["global_threshold"]
    min_count =         params_in["min_count"]
    gain =              params_in["gain"]
    size =              params_in["size"]
    n_iqr =             params_in["n_iqr"]
    blur =              params_in["blur"]
    n_bins =            params_in["n_bins"]

    experiments = ExperimentList.from_file(expt_path)
    my_imageset = experiments.imagesets()[0]

    detector = my_imageset.get_detector()
    print("len(detector obj) =", len(detector))

    obj_w_alg_lst = []
    for panel_number in range(len(detector)):
        flex_image = my_imageset.get_raw_data(on_sweep_img_num)[panel_number]
        try:
            mask_file = my_imageset.external_lookup.mask.filename
            pick_file = open(mask_file, "rb")
            mask_tup_obj = pickle.load(pick_file)
            pick_file.close()
            mask = mask_tup_obj[panel_number]

        except FileNotFoundError:
            mask = flex.bool(flex.grid(flex_image.all()),True)

        pars = (
            nsig_b, nsig_s, global_threshold, min_count, gain, size,
            n_iqr, blur, n_bins
        )

        obj_w_alg = from_image_n_mask_2_threshold(
            flex_image, mask, my_imageset, pars, panel_number
        )
        fin_mask = obj_w_alg.final_mask()
        obj_w_alg_lst.append(fin_mask)

    obj_w_alg_tup = tuple(obj_w_alg_lst)
    return obj_w_alg_tup



def get_bytes_w_2d_threshold_mask(
    experiments_list_path, img_num, params
):
    experiments = get_experiments(experiments_list_path[0])
    if experiments is not None:
        on_sweep_img_num, n_sweep = get_correct_img_num_n_sweep_num(
            experiments, img_num
        )

        tup_lst = get_dispersion_debug_obj_tup(
            expt_path = experiments_list_path[n_sweep],
            on_sweep_img_num = img_num,
            params_in = params
        )


        to_study_this = '''
        try:
            pick_file = open(mask_file, "rb")
            mask_tup_obj = pickle.load(pick_file)
            pick_file.close()

        except FileNotFoundError:
            logging.info("FileNotFoundError <<< get_bytes_w_2d_threshold_mask")
            mask_tup_obj = None

        byte_data, i23_multipanel = img_stream_py.mask_threshold_2_byte(
            img_tup_obj, mask_tup_obj, params, imageset_tmp
        )

        if byte_data == "Error":
            logging.info('byte_data == "Error"')
            byte_data = None


        return byte_data

    else:
        return None
        '''

    return tup_lst


if __name__ == "__main__":

    (experiments_list_path, img_num, params) = (
        ['/tmp/run_dui2_nodes/run4/masked.expt'],
        0,
        {
            'algorithm': 'radial_profile', 'nsig_b': 6.0, 'nsig_s': 3.0,
            'global_threshold': 0.0, 'min_count': 2, 'gain': 1.0,
            'size': (3, 3), 'n_iqr': 6, 'blur': None, 'n_bins': 100
        },
    )
    print("params =", params )
    for img_num_in in range(20):
        tuple_of_flex_mask = get_bytes_w_2d_threshold_mask(
            experiments_list_path, img_num_in, params
        )
        if len(tuple_of_flex_mask) == 24:
            print("24 panels, assuming i23 data(masking 1)")
            i23_multipanel = True
            np_arr = get_np_full_mask_from_i23_raw(tuple_of_flex_mask)

        else:
            print("Using the first panel only (masking 1)")
            data_xy_flex = tuple_of_flex_mask[0]
            np_arr = to_numpy(data_xy_flex)

        draw_pyplot(np_arr)


