import time

import img_stream_ext
import img_stream_py

import numpy as np
from dials.array_family import flex

import resource, sys

x_max = 3000
y_max = 3000
print("building data start")
data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        i = (x + y) / 2
        data_xyz_flex[x, y] = float(i)
print("building data end")

print("____________________________________________________________")
inv_scl, x1, y1, x2, y2 = 7, 4, 5, 2600, 2700

py_start_tm = time.time()
py_str_tst = img_stream_py.slice_arr_2_str(
    data_xyz_flex, inv_scl, x1, y1, x2, y2
)
py_end_tm = time.time()
print("scaling and converting in Python took ", py_end_tm - py_start_tm)
print(
    "py_str_tst ... =", py_str_tst[:70], "  ....  ", py_str_tst[-70:]
)

cpp_start_tm = time.time()
cpp_str_tst = img_stream_ext.slice_arr_2_str(
    data_xyz_flex, inv_scl, x1, y1, x2, y2
)
cpp_end_tm = time.time()
print("scaling and converting in C++ took ", cpp_end_tm - cpp_start_tm)
print(
    "cpp_str_tst ... =", cpp_str_tst[:70],    "  ....  ", cpp_str_tst[-70:]
)
