import numpy as np
from matplotlib import pyplot as plt
import tempfile

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
        tmp_fil, np_array_in,
        allow_pickle = False, fix_imports = False
    )

def save_comp_np_array(np_array_in):
    print("saving with allow_pickle = True")
    np.savez_compressed(
        tmp_fil, my_img = np_array_in, allow_pickle = True
    )

def load_np_array():
    img_arr_load = np.load(
        tmp_fil, mmap_mode = None, allow_pickle = False,
        fix_imports = False, encoding = 'ASCII'
    )
    return img_arr_load

def load_comp_np_array():
    print("opening with allow_pickle = True")
    dict_load = np.load(
        tmp_fil, mmap_mode = None, allow_pickle = True,
    )
    img_arr_load = dict_load["my_img"]
    return img_arr_load


if __name__ == "__main__":
    tmp_fil = tempfile.TemporaryFile()

    ncol = 190
    nrow = 70
    img_arr = build_img_arr(nrow, ncol)
    '''
    save_np_array(img_arr)
    tmp_fil.seek(0)
    loaded_array = load_np_array()
    '''
    save_comp_np_array(img_arr)
    tmp_fil.seek(0)
    loaded_array = load_comp_np_array()
    #'''

    draw_pyplot(loaded_array)
