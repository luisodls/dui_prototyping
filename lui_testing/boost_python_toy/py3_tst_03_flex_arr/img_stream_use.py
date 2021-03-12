import img_stream_ext
import numpy as np
from dials.array_family import flex

print(img_stream_ext.greet())

lst = [4,7,0]
a = img_stream_ext.lst_bunch(lst)
print("a =", a)

add_str = a[2] + a[3]
print("add_str =", add_str)

b = a[2].split(" ")
print("b =", b)

c = a[3].split(" ")
print("c =", c)

d = b + c
print("d =", d)

x_max = 8
y_max = 9
data_xyz_flex = flex.double(flex.grid(x_max, y_max), 0)
for x in range(x_max):
    for y in range(y_max):
        i = (x_max + y_max) - (abs(x_max / 2 - x) + abs(y_max / 2 - y))
        data_xyz_flex[x, y] = float(i)

print("data_xyz_flex = \n", data_xyz_flex.as_numpy_array())
