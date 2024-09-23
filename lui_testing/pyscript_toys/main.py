
import numpy as np
from matplotlib import pyplot as plt

siz0, siz1 = 15, 16
big_arr = np.zeros((siz0, siz1), dtype=np.double)

big_arr[4:9, 7:13] = 4
big_arr[7:13, 4:9] += 5

print("np_arr =\n", big_arr)

plt.imshow( big_arr , interpolation = "nearest" )
plt.show()

