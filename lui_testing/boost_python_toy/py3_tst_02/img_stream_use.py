import img_stream_ext
import numpy as np

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
