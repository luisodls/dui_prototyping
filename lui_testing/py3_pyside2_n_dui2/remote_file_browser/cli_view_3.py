import requests, json, os

def iter_gui(myself):
    if myself["isdir"]:
        print("\n DIR : ", myself["file_path"])

    else:
        print("file : ", myself["file_name"])

    for child in myself["list_child"]:
        if myself["isdir"]:
            iter_gui(child)


if __name__ == "__main__":
    print()

    path_in = input("path:")

    if path_in == "":
        path_in = os.environ.get('HOME')
        print("empty input for path replaced with ", path_in)

    req_get = requests.get(
        'http://localhost:8080/', stream = True,
        params = {"path":path_in}, timeout = 10
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
