import numpy as np
from matplotlib import pyplot as plt
import json

def build_img_arr(nrow, ncol):
    img_arr = np.zeros((nrow, ncol), dtype=float)

    for row in range(nrow):
        for col in range(ncol):
            img_arr[row, col] = row / 2 + col / 3

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

def save_json_w_str(np_array_in):
    d1 = np_array_in.shape[0]
    d2 = np_array_in.shape[1]
    arr_1d = np_array_in.reshape(d1 * d2)

    str_data = np.array2string(
        arr_1d, max_line_width = 15 * d1 * d2, precision = None,
        separator = ',', formatter={'float_kind':'{:10.3}'.format},
        threshold = d1 * d2, sign = None, legacy = None
    ).replace(' ', '')

    #print("str_data =", str_data)
    arr_dic = {"d1": d1, "d2": d2, "str_data": str_data}
    #print("\narr_dic =", arr_dic)

    with open("arr_img.json", "w") as fp:
        json.dump(arr_dic, fp, indent=4)


def load_json_w_str():

    with open("arr_img.json") as json_file:
        arr_dic = json.load(json_file)

    d1 = arr_dic["d1"]
    d2 = arr_dic["d2"]
    str_data = arr_dic["str_data"]
    print("d1, d2 =", d1, d2)
    print("str_data =", str_data)
    arr_1d = np.fromstring(str_data[1:-1], dtype = float, sep = ',')
    np_array_out = arr_1d.reshape(d1, d2)
    return np_array_out


if __name__ == "__main__":
    ncol = 200
    nrow = 120
    img_arr = build_img_arr(nrow, ncol)

    #draw_pyplot(img_arr)

    '''
    save_np_array(img_arr)
    loaded_array = load_np_array()

    draw_pyplot(loaded_array)
    '''

    save_json_w_str(img_arr)
    loaded_array = load_json_w_str()

    draw_pyplot(loaded_array)
