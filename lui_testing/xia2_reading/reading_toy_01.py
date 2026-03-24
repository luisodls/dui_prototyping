import sys

def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    log_file = open(path_in, 'r', encoding="utf-8")
    lines_str = log_file.readlines()
    log_file.close()
    list_of_commands = []
    for position, single_line in enumerate(lines_str):
        if single_line[0:15] == "# command line:":
            print()
            list_of_commands.append(lines_str[position + 1][1:])

    return list_of_commands


def main():
    try:
        lst_cmd = get_list_of_commands(sys.argv[1])
        for command in lst_cmd:
            print(command)

    except IndexError:
        print("Enter path of file to read")


if __name__ == "__main__":
    main()
