import img_stream_ext
import numpy as np
from dials.array_family import flex
from matplotlib import pyplot as plt
import json
import time
from dxtbx.model.experiment_list import ExperimentListFactory


def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def save_json_w_str(flex_array_in):
    d1, d2 = flex_array_in.all()
    print("d1, d2 =", d1, d2)
    start_tm = time.time()
    str_data = img_stream_ext.img_arr_2_str(flex_array_in)
    end_tm = time.time()
    print("C++ bit took ", end_tm - start_tm)

    print("str_data[0:80] =", str_data[0:80])
    print("str_data[-80:] =", str_data[-80:])

    with open("arr_img.json", 'w') as file_out:
        file_out.write(str_data + '\n')

def load_json_w_str():

    with open("arr_img.json") as json_file:
        arr_dic = json.load(json_file)

    d1 = arr_dic["d1"]
    d2 = arr_dic["d2"]
    str_data = arr_dic["str_data"]
    print("d1, d2 =", d1, d2)
    #print("str_data =", str_data)
    arr_1d = np.fromstring(str_data, dtype = float, sep = ',')
    np_array_out = arr_1d.reshape(d1, d2)
    #print("np_array_out =\n", np_array_out)
    return np_array_out


if __name__ == "__main__":
    experiments_path = "/scratch/dui_tst/dui_server_run/run1/imported.expt"
    print("importing from:", experiments_path)
    experiments = ExperimentListFactory.from_json_file(experiments_path)
    my_sweep = experiments.imagesets()[0]
    data_xy_flex = my_sweep.get_raw_data(0)[0].as_double()
    print("type(data_xy_flex) =", type(data_xy_flex))
    print("data_xy_flex.all() =", data_xy_flex.all())

    save_json_w_str(data_xy_flex)

    print("loading json")
    loaded_array = load_json_w_str()
    print("drawing")
    draw_pyplot(loaded_array)


