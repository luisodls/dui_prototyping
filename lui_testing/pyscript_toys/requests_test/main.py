
import numpy as np
from matplotlib import pyplot as plt

from tmp_lib import tst1

siz0, siz1 = 15, 16
big_arr = np.zeros((siz0, siz1), dtype=np.double)

big_arr[3:9, 7:13] = 4
big_arr[7:13, 3:9] += 5

tst1("luiso")

print("np_arr =\n", big_arr)

plt.imshow( big_arr , interpolation = "nearest" )
plt.show()

print("done")

