import lst_ext
import numpy as np

print(lst_ext.greet())

lst = [4,7,0]
a = lst_ext.lst_bunch(lst)
print("a =", a)

b = a[2].split(" ")
print("b =", b)
