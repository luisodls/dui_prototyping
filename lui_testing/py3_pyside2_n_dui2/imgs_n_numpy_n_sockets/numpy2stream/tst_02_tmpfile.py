import numpy as np
from matplotlib import pyplot as plt
import tempfile

def build_img_arr(nrow, ncol):
    img_arr = np.arange(nrow * ncol, dtype = float).reshape(nrow, ncol)
    img_arr[
        int(nrow / 4): int(nrow / 2),
        int(ncol / 4): int(ncol * 3 / 4)
    ] = np.max(img_arr)

    img_arr[
        int(nrow / 2): int(nrow * 3 / 4),
        int(ncol / 4): int(ncol * 3 / 4)
    ] = np.min(img_arr)

    print("\nimg_arr =\n", img_arr)
    return img_arr

def draw_pyplot(img_arr):
    print("\nimg_arr =\n",img_arr)
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def save_np_array(np_array_in):
    return np_array_in.tobytes(order='C')

def load_np_array(arr_bit):
    arr_1d = np.frombuffer(arr_bit, dtype = float)
    img_arr_load = arr_1d.reshape(8, 12)
    return img_arr_load

if __name__ == "__main__":
    tmp_fil = tempfile.TemporaryFile()

    nrow = 8
    ncol = 12
    img_arr = build_img_arr(nrow, ncol)

    bin_dat = save_np_array(img_arr)
    tmp_fil.seek(0)
    loaded_array = load_np_array(bin_dat)

    draw_pyplot(loaded_array)
