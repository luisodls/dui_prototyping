# run from parent dir (..)
# with command :
# dials.python -m client.client_main

import sys, os
from common.dep1 import dep01

if __name__ == "__main__":
    print("Hi from main client")
    dep01()
