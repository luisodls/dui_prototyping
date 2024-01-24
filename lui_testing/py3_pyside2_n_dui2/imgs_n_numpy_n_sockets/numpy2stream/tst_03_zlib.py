import numpy as np
from matplotlib import pyplot as plt

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

    #print("\nimg_arr =\n", img_arr)
    return img_arr

def draw_pyplot(img_arr):
    #print("\nimg_arr =\n",img_arr)
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def save_np_array(np_arr):
    d1 = np_arr.shape[0]
    d2 = np_arr.shape[1]
    img_arr = np.zeros(d1 * d2 + 2, dtype = float)
    img_arr[0] = float(d1)
    img_arr[1] = float(d2)
    img_arr[2:] = np_arr.ravel()
    byte_info = img_arr.tobytes(order='C')
    return byte_info

def load_np_array(arr_bit):
    arr_1d = np.frombuffer(arr_bit, dtype = float)
    img_arr_load = arr_1d[2:].reshape(
        int(arr_1d[0]), int(arr_1d[1])
    )
    return img_arr_load

if __name__ == "__main__":
    nrow = 900
    ncol = 1400
    img_arr = build_img_arr(nrow, ncol)
    bin_dat = save_np_array(img_arr)
    loaded_array = load_np_array(bin_dat)
    draw_pyplot(loaded_array)
