from dials.array_family import flex
from dxtbx.model.experiment_list import ExperimentListFactory

##############################################################################

import numpy as np
from matplotlib import pyplot as plt
import zlib

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



##############################################################################################
def get_experiments(experiment_path):
    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentListFactory.from_json_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments


if __name__ == "__main__":
    for img_num in range(20):
        print("got here #1")
        experiments = get_experiments(
            #"/scratch/30day_tmp/run_dui2_nodes/run1/imported.expt"
            "/tmp/run_dui2_nodes/run1/imported.expt"
        )
        print("got here #2")
        my_sweep = experiments.imagesets()[0]
        print("got here #3")
        raw_dat = my_sweep.get_raw_data(img_num)
        print("got here #4")
        data_xy_flex = raw_dat[0].as_double()
        print("got here #5")
        np_arr = data_xy_flex.as_numpy_array()
        print("got here #6")
        bin_dat = save_np_array(np_arr)
        print("got here #7")
        zcomp_data = zlib.compress(bin_dat)
        print("got here #8")
        decomp_data = zlib.decompress(zcomp_data)
        print("got here #9")
        loaded_array = load_np_array(decomp_data)
        print("got here #10")
        draw_pyplot(loaded_array)
        print("got here #11")



