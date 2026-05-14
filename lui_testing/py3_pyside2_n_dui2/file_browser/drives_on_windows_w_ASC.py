
import os

posible_drives = []
for asc_num in range(65, 91):
    posible_drives.append(chr(asc_num)+":")

print("posible_drives = ", posible_drives)

real_drives_lst = []
for tst_let in posible_drives:
    if os.path.isdir(tst_let):
        real_drives_lst.append(tst_let)

print("All real drives = ", real_drives_lst)

