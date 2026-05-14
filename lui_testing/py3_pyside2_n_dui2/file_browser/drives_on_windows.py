only_shows_C = '''
import psutil
drives = [drive.device for drive in psutil.disk_partitions()]
print(drives)
'''

lists_directily_C = '''
import os
print(os.listdir("/"))
'''

import os

list_of_posible_drives = [
    'A:','B:','C:','D:','E:','F:','G:','H:','I:','J:','K:','L:','M:'
    ,'N:','O:','P:','Q:','R:','S:','T:','U:','V:','W:','X:','Y:','Z:'
]
list_of_all_real_drives = []
for tst_let in list_of_posible_drives:
    if os.path.isdir(tst_let):
        list_of_all_real_drives.append(tst_let)

print("list of all real drives = ", list_of_all_real_drives)
