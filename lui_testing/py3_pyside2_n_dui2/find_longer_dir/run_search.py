copy_pasted = '''

    curr_path = uni_cmd[1].replace("/", os.sep)
    f_name_list =  os.listdir(curr_path)
    dict_list = []
    for f_name in f_name_list:
        f_path = curr_path + f_name
        f_isdir = os.path.isdir(f_path)
        file_dict = {"fname": f_name, "isdir":f_isdir}
        dict_list.append(file_dict)

    return_list = dict_list

'''

import os
longer_dir = ("~", 0)

def list_dir(path_in = "~"):
    try:
        f_name_list =  os.listdir(path_in)

    except (NotADirectoryError, FileNotFoundError):
        return

    len_lst = len(f_name_list)
    global longer_dir

    if len_lst > longer_dir[1]:
        longer_dir = (str(path_in), len_lst)
    print(
        "path_in =", path_in, " len(f_name_list) =", len_lst
    )
    lst_nxt_path = []
    for single_name in f_name_list:
        lst_nxt_path.append(path_in + os.sep + single_name)

    #print("lst_nxt_path =", lst_nxt_path)

    for lst_nxt_path in lst_nxt_path:
        list_dir(lst_nxt_path)

if __name__ == "__main__":
    list_dir(path_in = "/dls/i23/data/2024")
    #list_dir(path_in = "/dls/mx/data/mx37147")

    print("longer_dir =", longer_dir)
