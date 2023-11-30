import numpy as np
from matplotlib import pyplot as plt
import time

def build_img_arr(nrow, ncol):
    img_arr = np.arange(nrow * ncol).reshape(nrow, ncol)
    img_arr[
        int(nrow / 4): int(nrow / 2),
        int(ncol / 4): int(ncol * 3 / 4)
    ] = np.max(img_arr)

    img_arr[
        int(nrow / 2): int(nrow * 3 / 4),
        int(ncol / 4): int(ncol * 3 / 4)
    ] = np.min(img_arr)
    return img_arr

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def save_np_array(np_array_in):
    np.save(
        "arr_img", np_array_in,
        allow_pickle = False, fix_imports = False
    )

def save_comp_np_array(np_array_in):
    np.savez_compressed(
        "arr_img", my_img = np_array_in
    )

def load_np_array():
    img_arr_load = np.load(
        "arr_img.npy", mmap_mode = None, allow_pickle = False,
        fix_imports = False, encoding = 'ASCII'
    )
    return img_arr_load

def load_comp_np_array():
    dict_load = np.load(
        "arr_img.npz", mmap_mode = None, allow_pickle = False,
    )
    img_arr_load = dict_load["my_img"]
    return img_arr_load


if __name__ == "__main__":
    ncol = 530
    nrow = 380
    img_arr = build_img_arr(nrow, ncol)

    start_tm1 = time.time()
    save_np_array(img_arr)
    end_tm1 = time.time()
    acs_time = start_tm1 - end_tm1
    print("acs_time =", acs_time)

    loaded_asc_array = load_np_array()
    draw_pyplot(loaded_asc_array)

    start_tm2 = time.time()
    save_comp_np_array(img_arr)
    end_tm2 = time.time()
    comp_time = start_tm2 - end_tm1
    print("comp_time =", comp_time)

    loaded_comp_array = load_comp_np_array()
    draw_pyplot(loaded_comp_array)





