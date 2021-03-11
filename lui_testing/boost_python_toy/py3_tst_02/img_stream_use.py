import img_stream_ext
import numpy as np

print(img_stream_ext.greet())

lst = [4,7,0]
a = img_stream_ext.lst_bunch(lst)
print("a =", a)

b = a[2].split(" ")
print("b =", b)
