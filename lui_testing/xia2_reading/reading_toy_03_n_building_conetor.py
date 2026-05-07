import sys, os

def reversed_find_str(str_in = None, lst_sep_lst = ["=", os.sep]):
    final_str = str_in
    for pos, single_char in enumerate(reversed(str_in)):
        for char in lst_sep_lst:
            if single_char == char:
                final_str = str_in[-pos:]
                return final_str

    return final_str


def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    log_file = open(path_in, 'r', encoding="utf-8")
    lines_str = log_file.readlines()
    log_file.close()
    list_of_commands = []
    for position, single_line in enumerate(lines_str):
        if single_line[0:15] == "# command line:":
            print("\n")
            new_cmd_str = lines_str[position + 1][1:-1]
            print("<<", new_cmd_str, ">> \n")

            divide_pos = new_cmd_str.find("'")

            exe_cmd = new_cmd_str[0:divide_pos]
            print("exe_cmd =", exe_cmd)
            per_line_cmd_lst = new_cmd_str[divide_pos + 1:-1].split("' '")
            print("per_line_cmd_lst =", per_line_cmd_lst, "\n")

            full_cmd_lst = [exe_cmd]

            for inner_cmd in per_line_cmd_lst:
                if inner_cmd == "":
                    pass

                elif inner_cmd not in full_cmd_lst:
                    full_cmd_lst.append(inner_cmd)

            print("full_cmd_lst = ", full_cmd_lst)

            if exe_cmd == 'dials.report':
                print('exe_cmd = dials.report')
                continue

            connect_for_next_lst = []
            connect_from_prev_lst = []
            for single_par in full_cmd_lst:
                if "input" in single_par:
                    connect_from_prev_lst.append(single_par)

                if "output" in single_par:
                    connect_for_next_lst.append(single_par)

            for single_par in full_cmd_lst:
                if single_par[-5:] == ".refl" and (
                    single_par not in connect_from_prev_lst
                ) and (
                    single_par not in connect_for_next_lst
                ):
                    connect_from_prev_lst.append(single_par)

                if single_par[-5:] == ".expt" and (
                    single_par not in connect_from_prev_lst
                ) and (
                    single_par not in connect_for_next_lst
                ):
                    connect_from_prev_lst.append(single_par)

            expt_from_prev_lst = []
            refl_from_prev_lst = []
            another_from_prev_lst = []
            for par in connect_from_prev_lst:
                par = reversed_find_str(str_in = par)

                if par[-5:] == ".refl":
                    refl_from_prev_lst.append(par)

                elif par[-5:] == ".expt":
                    expt_from_prev_lst.append(par)

                else:
                    another_from_prev_lst.append(par)

            expt_for_next_lst = []
            refl_for_next_lst = []
            another_for_next_lst = []
            for par in connect_for_next_lst:
                par = reversed_find_str(str_in = par)
                if par[-5:] == ".refl":
                    refl_for_next_lst.append(par)

                elif par[-5:] == ".expt":
                    expt_for_next_lst.append(par)

                else:
                    another_for_next_lst.append(par)

            tuning_params_lst = []
            for single_par in full_cmd_lst:
                if(
                    (single_par not in exe_cmd) and
                    (single_par not in connect_from_prev_lst) and
                    (single_par not in connect_for_next_lst)
                ):
                    tuning_params_lst.append(single_par)

            #print("full_cmd_lst =", full_cmd_lst, "\n")

            cmd_dict = {
                'full_cmd_lst'              :full_cmd_lst,
                'exe_cmd'                   :exe_cmd,
                'expt_from_prev_lst'        :expt_from_prev_lst,
                'refl_from_prev_lst'        :refl_from_prev_lst,
                'another_from_prev_lst'     :another_from_prev_lst,
                'expt_for_next_lst'         :expt_for_next_lst,
                'refl_for_next_lst'         :refl_for_next_lst,
                'another_for_next_lst'      :another_for_next_lst,
                'tuning_params_lst'         :tuning_params_lst,
            }

            list_of_commands.append(cmd_dict)
    for cur_num, command_dict in enumerate(reversed(list_of_commands)):
        for prev_num, prev_com in enumerate(reversed(list_of_commands[0:cur_num - 1])):
            if command_dict['expt_from_prev_lst'] == prev_com['expt_for_next_lst']:
                print("connecting:" , prev_num, " with ", cur_num)

            if command_dict['refl_from_prev_lst'] == prev_com['refl_for_next_lst']:
                print("connecting:" , prev_num, " with ", cur_num)

    return list_of_commands


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        print("Enter path of file to read")
        lst_cmd = []

    else:
        lst_cmd = get_list_of_commands(arg_in)

    off_for_now = '''
    for pos_num, command in enumerate(lst_cmd):
        print("\n num =", pos_num, "\n", command, "\n")
    '''

    tmp_off = '''
    for pos_num, command in enumerate(lst_cmd):
        print(
            "\n num=<<", pos_num, ">>\nexe_cmd=<<", command["exe_cmd"],
             ">>\ninput=<<", command['connect_from_prev_lst'], ">>\n"
        )

        print(command)
    '''


if __name__ == "__main__":
    main()
