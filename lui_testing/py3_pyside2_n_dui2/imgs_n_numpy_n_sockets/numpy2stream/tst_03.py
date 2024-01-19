import numpy as np
from matplotlib import pyplot as plt
import time, io, zlib


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
    np.savez_compressed("arr_img", my_img = np_array_in)


def convert_to_ram_np_array(np_array_in):
    #mem_fil = io.BytesIO()
    mem_fil = io.FileIO(1)
    #mem_fil = io.StringIO()
    '''
    ['BlockingIOError', 'BufferedIOBase', 'BufferedRWPair', 'BufferedRandom', 'BufferedReader', 'BufferedWriter', 'BytesIO', 'DEFAULT_BUFFER_SIZE', 'FileIO', 'IOBase', 'IncrementalNewlineDecoder', 'RawIOBase', 'SEEK_CUR', 'SEEK_END', 'SEEK_SET', 'StringIO', 'TextIOBase', 'TextIOWrapper', 'UnsupportedOperation', '__all__', '__author__', '__builtins__', '__doc__', '__file__', '__getattr__', '__loader__', '__name__', '__package__', '__spec__', '_io', 'abc', 'open', 'open_code', 'text_encoding']
    '''
    np.savez_compressed(mem_fil, my_img = np_array_in)
    print("len(mem_fil) =", len(mem_fil))
    return mem_fil



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

def convert_back(img_in):
    '''dict_load = np.load(
        img_in, mmap_mode = None, allow_pickle = False,
    )'''
    print("len(img_in) =", len(img_in))
    print("type(img_in) =", type(img_in))
    dict_load = np.load(img_in)
    img_arr_load = dict_load["my_img"]
    return img_arr_load


if __name__ == "__main__":
    ncol = 530
    nrow = 380
    img_arr = build_img_arr(nrow, ncol)
    '''
    start_tm1 = time.time()
    save_np_array(img_arr)
    end_tm1 = time.time()
    acs_time = start_tm1 - end_tm1
    print("acs_time =", acs_time)

    loaded_asc_array = load_np_array()
    draw_pyplot(loaded_asc_array)
    '''

    bit_img = convert_to_ram_np_array(img_arr)
    print("1")
    loaded_bin_array = convert_back(bit_img)
    print("2")
    draw_pyplot(loaded_bin_array)
    print("3")

    '''
    start_tm2 = time.time()
    save_comp_np_array(img_arr)
    end_tm2 = time.time()
    comp_time = start_tm2 - end_tm1
    print("comp_time =", comp_time)

    loaded_comp_array = load_comp_np_array()
    draw_pyplot(loaded_comp_array)
    '''





