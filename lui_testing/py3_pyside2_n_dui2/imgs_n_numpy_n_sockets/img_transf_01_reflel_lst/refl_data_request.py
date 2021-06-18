import json
import requests

def json_data_request(url, cmd):
    '''
    this is a carbon copy of the function in upstream DUI2
    '''
    try:
        req_get = requests.get(url, stream = True, params = cmd, timeout = 3)
        str_lst = ''
        line_str = ''

        #while True:
        times_loop = 10
        json_out = ""
        for count_times in range(times_loop):
            tmp_dat = req_get.raw.readline()
            line_str = str(tmp_dat.decode('utf-8'))
            if line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

            else:
                str_lst = line_str

            if count_times == times_loop - 1:
                print('to many "lines" in http response')
                json_out = None

        if json_out is not None:
            json_out = json.loads(str_lst)

    except ConnectionError:
        print("\n ConnectionError (json_data_request) \n")
        json_out = None

    except requests.exceptions.RequestException:
        print("\n requests.exceptions.RequestException (json_data_request) \n")
        json_out = None

    return json_out


if __name__ == "__main__":
    my_cmd = {'nod_lst': [12], 'cmd_lst': ["grl 0"]}
    json_lst = json_data_request('http://localhost:8080/', my_cmd)
    for inner_list in json_lst[0:5]:
        print("\n inner_list =", inner_list)
        lst_str1 = inner_list[0].split(',')
        print("lst_str1 =", lst_str1)
        x_ini = float(lst_str1[0])
        y_ini = float(lst_str1[1])
        xrs_size = int(lst_str1[2])
        size2 = int(lst_str1[3])
        local_hkl = str(inner_list[1])

        print("x_ini =     ", x_ini    )
        print("y_ini =     ", y_ini    )
        print("xrs_size =  ", xrs_size )
        print("size2 =     ", size2    )
        print("local_hkl = ", local_hkl)


'''
json_lst = [['850.26,578.12,3,2', '(-20, 10, -12)'], ['1258.65,582.44,3,2', '(-22, 0, -4)'], ['1006.61,656.33,3,2', '(-19, 7, -8)'], ['1200.78,655.23,3,2', '(-20, 2, -4)'], ['1306.23,670.43,3,2', '(-20, -1, -2)'], ['1091.22,673.89,3,2', '(-19, 5, -6)'], ['
'''


