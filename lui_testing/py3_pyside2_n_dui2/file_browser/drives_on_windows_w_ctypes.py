# Copy/Pasted from on-line example:
import ctypes
import string

def get_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

# Usage
print(get_drives())
# Output: ['C:\\', 'D:\\', ...]
