import requests, json


def iter_gui(myself):
    if myself["isdir"]:
        stat = "DIR"

    else:
        stat = " file"

    print(stat, " : ", myself["file_name"])
    for child in myself["list_child"]:
        if myself["isdir"]:
            iter_gui(child)

if __name__ == "__main__":

    req_get = requests.get(
        'http://localhost:8080/', stream = True,
        params = {"path":"/scratch/dui_tst/"}, timeout = 3
    )
    str_lst = ''
    line_str = ''
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
        iter_gui(json_out)
