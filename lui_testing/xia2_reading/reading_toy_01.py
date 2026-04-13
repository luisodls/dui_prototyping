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

            for inner_cmd in per_line_cmd_lst:
                if inner_cmd == '':
                    per_line_cmd_lst.remove(inner_cmd)

            print("per_line_cmd_lst(after) =", per_line_cmd_lst, "\n")
            list_of_commands.append(per_line_cmd_lst)

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
