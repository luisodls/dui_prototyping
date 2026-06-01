I am considering the following code for a multi platform solution


import ctypes
import string
import os

def get_drives():
    drives = []
    try:
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives

    except AttributeError:
        # NOT running on windows"
        return sorted(os.listdir("/"))

# Usage
print(get_drives())
# Output: ['C:\\', 'D:\\', ...]
