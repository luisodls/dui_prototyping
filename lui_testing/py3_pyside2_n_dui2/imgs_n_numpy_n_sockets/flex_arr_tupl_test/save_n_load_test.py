import numpy as np
'''
import msgpack_numpy as m
import msgpack
'''
from dials.array_family import flex
from matplotlib import pyplot as plt
import time, zlib, json
from dxtbx.model.experiment_list import ExperimentListFactory

def build_img_arr(nrow, ncol):
    data_xy_flex = flex.double(flex.grid(nrow, ncol), 0)
    for col in range(nrow):
        for row in range(ncol):
            i = (col + row) / 3
            data_xy_flex[col, row] = float(i)
    return data_xy_flex

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()


def save_tup_str(data_xy_flex):
    start_tm = time.time()
    np_arr = data_xy_flex.as_numpy_array()
    d1 = np_arr.shape[0]
    d2 = np_arr.shape[1]
    str_tup = str(tuple(np_arr.ravel()))
    str_data = "{\"d1\":" + str(d1) + ",\"d2\":" + str(d2) \
             + ",\"str_data\":\"" + str_tup[1:-1] + "\"}"

    byt_data = bytes(str_data.encode('utf-8'))
    compresed = zlib.compress(byt_data)
    end_tm = time.time()
    print("str/tuple use and compressing took ", end_tm - start_tm)
    with open("arr_img.json.zip", 'wb') as file_out:
        file_out.write(compresed)


def load_json_w_str():
    with open("arr_img.json.zip", 'rb') as json_file:
        compresed = json_file.read()

    dic_str = zlib.decompress(compresed)
    arr_dic = json.loads(dic_str)

    d1 = arr_dic["d1"]
    d2 = arr_dic["d2"]
    str_data = arr_dic["str_data"]
    print("d1, d2 =", d1, d2)
    arr_1d = np.fromstring(str_data, dtype = float, sep = ',')
    np_array_out = arr_1d.reshape(d1, d2)
    return np_array_out


if __name__ == "__main__":
    #data_xy_flex = build_img_arr(18,36)

    experiments_path = "/home/lui/diff_data/temp_run/imported.expt"
    #experiments_path = "/scratch/dui_tst/dui_server_run/run1/imported.expt"

    print("importing from:", experiments_path)
    experiments = ExperimentListFactory.from_json_file(experiments_path)
    my_sweep = experiments.imagesets()[0]
    data_xy_flex = my_sweep.get_raw_data(0)[0].as_double()
    print("type(data_xy_flex) =", type(data_xy_flex))
    print("data_xy_flex.all() =", data_xy_flex.all())

    np_arr = data_xy_flex.as_numpy_array()

    save_tup_str(data_xy_flex)
    np_rec = load_json_w_str()
    draw_pyplot(np_rec)

