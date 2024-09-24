

def get(url = None, stream = False, params = None):
    print("url =", url)
    print("stream =", stream)
    print("params =", params)


'''
while True:
    tmp_dat = req_get.raw.readline()
    print("tmp_dat =", tmp_dat)
    line_str = str(tmp_dat.decode('utf-8'))
    if '/*EOF*/' in line_str:
        print('/*EOF*/ received')
        break

    else:
        print(str(line_str[:-1]))

'''
