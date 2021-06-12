import img_stream_ext
#import numpy as np
from dials.array_family import flex
from matplotlib import pyplot as plt


def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()

if __name__ == "__main__":
    x_max = 2400
    y_max = 1600
    data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
    for x in range(x_max):
        for y in range(y_max):
            i = (x + y) / 2
            data_xyz_flex[x, y] = float(i)

    draw_pyplot(data_xyz_flex.as_numpy_array())

    print("before img_arr_2_str  ...")
    tst_str = img_stream_ext.img_arr_2_str(data_xyz_flex)
    print("...  after img_arr_2_str")
    print("tst_str =", tst_str)
