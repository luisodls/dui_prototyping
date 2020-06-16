# run from parent dir (..)
# with command :
# dials.python -m server.server_main

import sys, os
try:
    from common.dep1 import dep01

except:
    sys.path.append('/scratch/dui_prototyping/lui_testing/python_mic/py_dir_n_deps/common')
    from dep1 import dep01

if __name__ == "__main__":
    print("Hi from main server")
    dep01()

    print(dir(sys))
