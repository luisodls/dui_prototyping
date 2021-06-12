import numpy as np
import msgpack_numpy as m
from dials.array_family import flex
from matplotlib import pyplot as plt
import time, msgpack, zlib
from dxtbx.model.experiment_list import ExperimentListFactory

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

def save_msgpack(flex_arr_in):
    start_tm = time.time()

    np_arr = flex_arr_in.as_numpy_array()
    np_enc = msgpack.packb(np_arr, default=m.encode)
    print("type(np_enc) =", type(np_enc))
    compresed = zlib.compress(np_enc)
    print("type(compresed) =", type(compresed))
    end_tm = time.time()
    print("packing/compresing took ", end_tm - start_tm)

    with open("arr_img.msg", 'wb') as file_out:
        file_out.write(compresed)

def load_msgpack():
    with open("arr_img.msg", 'rb') as msg_file:
        compresed = msg_file.read()

    start_tm = time.time()

    np_enc = zlib.decompress(compresed)
    np_rec = msgpack.unpackb(np_enc, object_hook=m.decode)

    end_tm = time.time()
    print("unpacking/decompresing took ", end_tm - start_tm)

    return np_rec

if __name__ == "__main__":
    experiments_path = "/scratch/dui_tst/dui_server_run/run1/imported.expt"
    print("importing from:", experiments_path)
    experiments = ExperimentListFactory.from_json_file(experiments_path)
    my_sweep = experiments.imagesets()[0]
    data_xy_flex = my_sweep.get_raw_data(0)[0].as_double()
    print("type(data_xy_flex) =", type(data_xy_flex))
    print("data_xy_flex.all() =", data_xy_flex.all())

    draw_pyplot(data_xy_flex.as_numpy_array())
    save_msgpack(data_xy_flex)
    np_rec = load_msgpack()
    draw_pyplot(np_rec)

