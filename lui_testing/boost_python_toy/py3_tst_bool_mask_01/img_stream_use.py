import time

import img_stream_ext
import img_stream_py

import numpy as np
from dials.array_family import flex

import resource, sys

x_max = 1600
y_max = 1200
print("building data start")
data_bool_flex = flex.bool(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        if x > y:
            data_bool_flex[x, y] = True

        else:
            data_bool_flex[x, y] = False

#print("data in =\n", data_bool_flex.as_numpy_array())

cpp_str_tst = img_stream_ext.mask_arr_2_str(data_bool_flex)
py_str_tst = img_stream_py.mask_arr_2_str(data_bool_flex)

print("len(cpp_str_tst) =", len(cpp_str_tst))
#print( "cpp_str_tst =", cpp_str_tst)
print( "cpp_str_tst =", cpp_str_tst[:50], " ... ", cpp_str_tst[-50:])
print("len(py_str_tst) =", len(py_str_tst))
#print( "py_str_tst  =", py_str_tst)
print( "py_str_tst  =", py_str_tst[:50], py_str_tst[-50:])
#########################################################################
for inv_scale in range(1, 40, 1):
    cpp_start_tm = time.time()
    scaled_cpp_str = img_stream_ext.slice_mask_2_str(
        data_bool_flex, inv_scale, 3, 4, 1500, 1100
    )
    cpp_end_tm = time.time() - cpp_start_tm

    py_start_tm = time.time()
    scaled_py_str = img_stream_py.slice_mask_2_str(
        data_bool_flex, inv_scale, 3, 4, 1500, 1100
    )
    py_end_tm = time.time() - py_start_tm

    print("len(scaled_cpp_str) =", len(scaled_cpp_str))
    print("scaled_cpp_str =", scaled_cpp_str[:50], " ... ", scaled_cpp_str[-50:])
    print("cpp_end_tm =", cpp_end_tm)
    print("len(scaled_py_str) =", len(scaled_py_str))
    print("scaled_py_str =", scaled_py_str[:50], " ... ", scaled_py_str[-50:])
    print("py_end_tm =", py_end_tm)
