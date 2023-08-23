import psutil
import sys
import os

pid = int(os.getpid())
print("pid(me) =", pid)

for singl_proc in psutil.process_iter():
    lst4cmd = singl_proc.cmdline()
    try:
        if lst4cmd[-1][-12:] == "all_local.py":
            print("\nlst4cmd =", lst4cmd)
            print("pid =", int(singl_proc.pid), "\n")
            #print(dir(singl_proc))

    except IndexError:
        pass

