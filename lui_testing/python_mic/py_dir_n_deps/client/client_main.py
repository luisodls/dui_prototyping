# run from parent dir (..)
# with command :
# dials.python -m client.client_main

import sys, os
try:
    from common.dep1 import dep01

except ModuleNotFoundError:
    comm_path = os.path.abspath(__file__)[0:-21] + "common"
    sys.path.append(comm_path)
    from dep1 import dep01


if __name__ == "__main__":
    print("Hi from main client")
    dep01()
