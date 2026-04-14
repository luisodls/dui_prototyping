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

            par_lst = []
            for inner_cmd in per_line_cmd_lst:
                if inner_cmd == '':
                    per_line_cmd_lst.remove(inner_cmd)

                elif inner_cmd[-1] == "'":
                    par_lst.append(inner_cmd[1:-1])

            print("per_line_cmd_lst(after) =", per_line_cmd_lst, "\n")
            cmd_dict = {
                'exe_cmd'       :per_line_cmd_lst[0],
                'par_lst'   :par_lst
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
        lst_cmd = get_list_of_commands(sys.argv[1])

    except IndexError:
        print("Enter path of file to read")
        lst_cmd = []

    for command in lst_cmd:
        print(command)


if __name__ == "__main__":
    main()
