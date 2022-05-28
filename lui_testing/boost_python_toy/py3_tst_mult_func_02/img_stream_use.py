import img_stream_ext
import numpy as np
from dials.array_family import flex

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

print(img_stream_ext.greet())

x_max = 4000
y_max = 3000
print("building data start")
data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        i = (x + y) / 2
        data_xyz_flex[x, y] = float(i)
print("building data end")

print("data_xyz_flex = \n", data_xyz_flex.as_numpy_array())
print("cadena1 =", img_stream_ext.cadena1())
print("here 1")
str_tst = img_stream_ext.build_str(data_xyz_flex)
print("here 2")
print("len(str_tst) =", len(str_tst), ">>")
