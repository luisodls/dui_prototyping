
#import img_stream_ext
import img_stream_py

import numpy as np
from dials.array_family import flex

import resource, sys

x_max = 6
y_max = 5
print("building data start")
data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        i = (x + y) / 2
        data_xyz_flex[x, y] = float(i)
print("building data end")
'''
small_str_tst = img_stream_ext.slice_arr_2_str(
    data_xyz_flex, 1, 25, 35, 45, 55
)'''
small_str_tst = img_stream_py.slice_arr_2_str(
    data_xyz_flex, 1, 25, 35, 45, 55
)
print("small_str_tst =", small_str_tst)
print(
    "small_str_tst ... =", small_str_tst[0:25],
    "  ...  ", small_str_tst[-25:len(small_str_tst)]
)
print("____________________________________________________________")
'''
big_str_tst = img_stream_ext.slice_arr_2_str(
    data_xyz_flex, 1, 25, 35, 2500, 2500
)
big_str_tst = img_stream_py.slice_arr_2_str(
    data_xyz_flex, 1, 25, 35, 2500, 2500
)
print("len(big_str_tst) =", len(big_str_tst), ">>")

print(
    "big_str_tst ... =", big_str_tst[0:50],
    "  ....  ", big_str_tst[-50:len(big_str_tst)]
)
'''
