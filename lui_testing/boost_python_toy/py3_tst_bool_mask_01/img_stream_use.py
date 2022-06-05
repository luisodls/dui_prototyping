import time

import img_stream_ext
import img_stream_py

import numpy as np
from dials.array_family import flex

import resource, sys

x_max = 3000
y_max = 3000
print("building data start")
data_bool_flex = flex.bool(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        if float(x+y) / 2.0 == int((x+y)/2):
            data_bool_flex[x, y] = True

        else:
            data_bool_flex[x, y] = False

print("data_bool_flex =\n", data_bool_flex.as_numpy_array())

cpp_start_tm = time.time()
cpp_str_tst = img_stream_ext.mask_arr_2_str(data_bool_flex)
cpp_end_tm = time.time()


py_start_tm = time.time()
py_str_tst = img_stream_py.mask_arr_2_str(data_bool_flex)
py_end_tm = time.time()

print("converting in C++ took ", cpp_end_tm - cpp_start_tm)
print("converting in Python took ", py_end_tm - py_start_tm)

print( "cpp_str_tst =", cpp_str_tst[:50], "  ...  ", cpp_str_tst[-50:])
print( "py_str_tst  =", py_str_tst[:50], "  ...  ", py_str_tst[-50:])

