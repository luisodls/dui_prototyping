import sys

def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    log_file = open(path_in, 'r', encoding="utf-8")
    lines_str = log_file.readlines()
    log_file.close()
    list_of_commands = []
    for position, single_line in enumerate(lines_str):
        if single_line[0:15] == "# command line:":
            print("\n\n")
            new_cmd_str = lines_str[position + 1][1:-1]
            print("<<", new_cmd_str, ">> \n")
            per_line_cmd_lst = new_cmd_str.split(" ")


            full_cmd_lst = []
            for inner_cmd in per_line_cmd_lst:
                if inner_cmd == "":
                    pass

                elif inner_cmd[0] == "'":
                    full_cmd_lst.append(inner_cmd[1:-1])

                else:
                    exe_cmd = inner_cmd
                    full_cmd_lst.append(inner_cmd)

            conect_for_next_lst = []
            connect_from_prev_lst = []
            for single_par in full_cmd_lst:
                if "input" in single_par:
                    connect_from_prev_lst.append(single_par)

                if "output" in single_par:
                    conect_for_next_lst.append(single_par)

            for single_par in full_cmd_lst:
                if single_par[-5:] == ".refl" and (
                    single_par not in connect_from_prev_lst
                ) and (
                    single_par not in conect_for_next_lst
                ):
                    connect_from_prev_lst.append(single_par)

                if single_par[-5:] == ".expt" and (
                    single_par not in connect_from_prev_lst
                ) and (
                    single_par not in conect_for_next_lst
                ):
                    connect_from_prev_lst.append(single_par)
            tuning_params_lst = []
            for single_par in full_cmd_lst:
                if(
                    (single_par not in exe_cmd) and
                    (single_par not in connect_from_prev_lst) and
                    (single_par not in conect_for_next_lst)
                ):
                    tuning_params_lst.append(single_par)


            print("connect_from_prev_lst =", connect_from_prev_lst, "\n")
            print("conect_for_next_lst =", conect_for_next_lst, "\n")

            print("full_cmd_lst =", full_cmd_lst, "\n")

            cmd_dict = {
                'full_cmd_lst'              :full_cmd_lst,
                'exe_cmd'                   :exe_cmd,
                'connect_from_prev_lst'     :connect_from_prev_lst,
                'conect_for_next_lst'       :conect_for_next_lst,
                'tuning_params_lst'              :tuning_params_lst,
            }
            if len(cmd_dict['exe_cmd']) > 6:
                if cmd_dict['exe_cmd'][0:6] == "dials.":
                    cmd_dict['dials_cmd'] = cmd_dict['exe_cmd'][6:]

                else:
                    cmd_dict['dials_cmd'] = False

            else:
                cmd_dict['dials_cmd'] = False

            list_of_commands.append(cmd_dict)

    return list_of_commands


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        print("Enter path of file to read")
        lst_cmd = []

    else:
        lst_cmd = get_list_of_commands(arg_in)

    for command in lst_cmd:
        print(command, "\n")


if __name__ == "__main__":
    main()
