# multi platform way to take the user to the "root" dir

import platform
import os

def get_drives():
    system = platform.system()

    if system == "Windows":
        import ctypes, string
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives

    else:
        return sorted(os.listdir("/"))

print(get_drives())

