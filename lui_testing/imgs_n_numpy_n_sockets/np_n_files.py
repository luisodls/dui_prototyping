import numpy as np
from matplotlib import pyplot as plt

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
        "arr_img.npy", np_array_in,
        allow_pickle = False, fix_imports = False
    )

def load_np_array():
    img_arr_load = np.load(
        "arr_img.npy", mmap_mode = None, allow_pickle = False,
        fix_imports = False, encoding = 'ASCII'
    )
    return img_arr_load


if __name__ == "__main__":
    ncol = 50
    nrow = 30
    img_arr = build_img_arr(nrow, ncol)

    save_np_array(img_arr)
    loaded_array = load_np_array()

    draw_pyplot(loaded_array)
