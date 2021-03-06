import img_stream_ext
import numpy as np
from dials.array_family import flex

print(img_stream_ext.greet())

x_max = 16
y_max = 12
data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        i = (x + y) / 2
        data_xyz_flex[x, y] = float(i)

print("data_xyz_flex = \n", data_xyz_flex.as_numpy_array())

tst = img_stream_ext.lst_bunch(data_xyz_flex)
print("tst =", tst)
