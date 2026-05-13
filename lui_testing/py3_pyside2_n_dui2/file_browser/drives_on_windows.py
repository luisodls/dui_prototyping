import psutil
drives = [drive.device for drive in psutil.disk_partitions()]
print(drives)

list_directily_C = '''
import os
print(os.listdir("/"))
'''
