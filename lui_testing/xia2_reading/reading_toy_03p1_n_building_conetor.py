import sys, os

# parts of a parameter name (before "=") that mark it as a written file
# e.g.: output.experiments=..., mtz.hklout=..., json=...
OUTPUT_KEY_PARTS = ["output", "hklout", "json"]

# CCP4 style positional pairs, e.g.: freerflag 'hklin' 'a.mtz' 'hklout' 'b.mtz'
POSITIONAL_IN = ["hklin", "xyzin"]
POSITIONAL_OUT = ["hklout", "xyzout"]

FILE_EXTENSIONS = [
    ".expt", ".refl", ".mtz", ".mmcif", ".cif", ".json", ".phil",
    ".mask", ".sca", ".p4p", ".html", ".log", ".bz2",
]


def reversed_find_str(str_in = None, lst_sep_lst = ["=", os.sep]):
    final_str = str_in
    for pos, single_char in enumerate(reversed(str_in)):
        for char in lst_sep_lst:
            if single_char == char:
                final_str = str_in[len(str_in) - pos:]
                return final_str

    return final_str


def is_output_key(key):
    if key.endswith("hklout"):
        return True

    for part in key.split("."):
        if part in OUTPUT_KEY_PARTS:
            return True

    return False


def has_file_extension(file_name):
    for ext in FILE_EXTENSIONS:
        if file_name.endswith(ext):
            return True

    return False


def is_bravais_setting(file_name):
    prefix, suffix = "bravais_setting_", ".expt"
    if not (file_name.startswith(prefix) and file_name.endswith(suffix)):
        return False

    return file_name[len(prefix):-len(suffix)].isdecimal()


# files written with default names that never appear as output parameters,
# (test on the file name, program that wrote it)
IMPLICIT_OUTPUTS = [
    (is_bravais_setting, "dials.refine_bravais_settings"),
]


def split_cmd_line(new_cmd_str):
    new_cmd_str = new_cmd_str.strip()
    divide_pos = new_cmd_str.find("'")
    if divide_pos == -1:
        # command without arguments, e.g.: xia2.report
        return new_cmd_str, [new_cmd_str]

    exe_cmd = new_cmd_str[0:divide_pos].strip()
    per_line_cmd_lst = new_cmd_str[divide_pos + 1:-1].split("' '")

    full_cmd_lst = [exe_cmd]
    for inner_cmd in per_line_cmd_lst:
        if inner_cmd == "":
            pass

        elif inner_cmd not in full_cmd_lst:
            full_cmd_lst.append(inner_cmd)

    return exe_cmd, full_cmd_lst


def classify_params(full_cmd_lst):
    connect_from_prev_lst = []
    connect_for_next_lst = []
    tuning_params_lst = []
    par_lst = full_cmd_lst[1:]
    skip_next = False
    for pos, single_par in enumerate(par_lst):
        if skip_next:
            skip_next = False

        elif (
            single_par in POSITIONAL_IN + POSITIONAL_OUT
            and pos + 1 < len(par_lst)
        ):
            if single_par in POSITIONAL_OUT:
                connect_for_next_lst.append(par_lst[pos + 1])

            else:
                connect_from_prev_lst.append(par_lst[pos + 1])

            skip_next = True

        elif "=" in single_par:
            key = single_par[0:single_par.find("=")]
            file_name = reversed_find_str(str_in = single_par)
            if is_output_key(key) and "." in file_name:
                connect_for_next_lst.append(single_par)

            elif "input" in key or has_file_extension(file_name):
                connect_from_prev_lst.append(single_par)

            else:
                # includes non file outputs like output.project_name=...
                tuning_params_lst.append(single_par)

        elif has_file_extension(reversed_find_str(str_in = single_par)):
            connect_from_prev_lst.append(single_par)

        else:
            tuning_params_lst.append(single_par)

    return connect_from_prev_lst, connect_for_next_lst, tuning_params_lst


def split_by_type(par_lst):
    expt_lst = []
    refl_lst = []
    another_lst = []
    for par in par_lst:
        par = reversed_find_str(str_in = par)
        if par[-5:] == ".refl":
            refl_lst.append(par)

        elif par[-5:] == ".expt":
            expt_lst.append(par)

        else:
            another_lst.append(par)

    return expt_lst, refl_lst, another_lst


def find_implicit_parent(file_name, prev_cmd_lst):
    for matches, exe_cmd in IMPLICIT_OUTPUTS:
        if matches(file_name):
            # most recent previous run of that program
            for prev_dict in reversed(prev_cmd_lst):
                if prev_dict['exe_cmd'] == exe_cmd:
                    return prev_dict['curr_poss']

    return None


def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    log_file = open(path_in, 'r', encoding="utf-8")
    lines_str = log_file.readlines()
    log_file.close()
    list_of_commands = []
    curr_poss = 0
    for position, single_line in enumerate(lines_str):
        if single_line[0:15] == "# command line:":
            print("\n")
            new_cmd_str = lines_str[position + 1][1:]
            exe_cmd, full_cmd_lst = split_cmd_line(new_cmd_str)

            if exe_cmd == 'dials.report':
                #TODO: have a look if some command escapes this
                continue

            (
                connect_from_prev_lst, connect_for_next_lst, tuning_params_lst
            ) = classify_params(full_cmd_lst)

            (
                expt_from_prev_lst, refl_from_prev_lst, another_from_prev_lst
            ) = split_by_type(connect_from_prev_lst)

            (
                expt_for_next_lst, refl_for_next_lst, another_for_next_lst
            ) = split_by_type(connect_for_next_lst)

            print("full_cmd_lst", curr_poss, " = ", full_cmd_lst, "\n")

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
                'parent_pos_lst'            :[],
                'chidren_pos_lst'           :[],
                'files_from_parent_dict'    :{},
                'external_files_lst'        :[],
                'curr_poss'                 :curr_poss,
            }
            curr_poss += 1
            list_of_commands.append(cmd_dict)

    print("\n", "=" * 90)

    # file name -> position of the most recent command that wrote it
    producer_of = {}
    for cur_num, curr_dict in enumerate(list_of_commands):
        for file_name in (
            curr_dict['expt_from_prev_lst'] +
            curr_dict['refl_from_prev_lst'] +
            curr_dict['another_from_prev_lst']
        ):
            if file_name in producer_of:
                parent_poss = producer_of[file_name]

            else:
                parent_poss = find_implicit_parent(
                    file_name, list_of_commands[0:cur_num]
                )

            if parent_poss is None:
                curr_dict['external_files_lst'].append(file_name)
                continue

            if parent_poss not in curr_dict['parent_pos_lst']:
                curr_dict['parent_pos_lst'].append(parent_poss)
                parent_dict = list_of_commands[parent_poss]
                parent_dict['chidren_pos_lst'].append(curr_dict['curr_poss'])
                curr_dict['files_from_parent_dict'][parent_poss] = []

            curr_dict['files_from_parent_dict'][parent_poss].append(file_name)

        for file_name in (
            curr_dict['expt_for_next_lst'] +
            curr_dict['refl_for_next_lst'] +
            curr_dict['another_for_next_lst']
        ):
            producer_of[file_name] = curr_dict['curr_poss']

    for curr_dict in list_of_commands:
        for parent_poss in curr_dict['parent_pos_lst']:
            print(
                "connecting: ", parent_poss, " with ", curr_dict['curr_poss'],
                " via ", curr_dict['files_from_parent_dict'][parent_poss]
            )

    print("\n", "=" * 90)

    tmp_off = '''for cmd_dict in list_of_commands:
        for parent_poss in cmd_dict['parent_pos_lst']:
            print(
                "\n", list_of_commands[parent_poss]['full_cmd_lst'],
                "\nconnects to:\n", cmd_dict['full_cmd_lst'], "\n"
            )

        if cmd_dict['external_files_lst'] != []:
            print(
                "\n", cmd_dict['full_cmd_lst'], "\nreads external files:\n",
                cmd_dict['external_files_lst'], "\n"
            )

    print("\n", "+" * 90)

    for cmd_dict in list_of_commands:
        for child_poss in cmd_dict['chidren_pos_lst']:
            print(
                "\n", cmd_dict['full_cmd_lst'], "\nconnects to:\n",
                list_of_commands[child_poss]['full_cmd_lst'], "\n"
            )'''


    return list_of_commands


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        print("Enter path of file to read ... /xia2-debug.txt")
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
