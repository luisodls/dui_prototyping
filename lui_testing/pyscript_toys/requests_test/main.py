
import numpy as np
from matplotlib import pyplot as plt

#from tmp_lib import tst1

import tmp_lib as requests

if __name__ == "__main__":
    uni_url = 'http://127.0.0.1:45678/'
    full_cmd = {"nod_lst":"", "cmd_str":["dir_path"]}
    req_get = requests.get(uni_url, stream = True, params = full_cmd)

    print("done")




