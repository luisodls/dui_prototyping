

def get(
    url = None, params = None, allow_redirects = True,
    auth = None, cert = None, cookies = None, headers = None,
    proxies = None, stream = False, timeout = None, verify = True,
):
    print("url =             ", url              )
    print("params =          ", params           )
    print("allow_redirects = ", allow_redirects  )
    print("auth =            ", auth             )
    print("cert =            ", cert             )
    print("cookies =         ", cookies          )
    print("headers =         ", headers          )
    print("proxies =         ", proxies          )
    print("stream =          ", stream           )
    print("timeout =         ", timeout          )
    print("verify =          ", verify           )



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
