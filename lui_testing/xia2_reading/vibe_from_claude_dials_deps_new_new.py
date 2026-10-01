import sys, os, json

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

# commands without arguments that work on what the previous command wrote,
# e.g.: convert-mtz-sca converts the .mtz just written by dials.export/merge
USES_PREVIOUS_OUTPUT = ["convert-mtz-sca"]

# parameters whose value is a result of a previous program, not a file,
# (parameter name, programs whose most recent run gave that value)
PARAM_FROM_PROGRAM = [
    (
        "change_of_basis_op",
        ["dials.refine_bravais_settings", "dials.symmetry"],
    ),
    ("space_group", ["dials.refine_bravais_settings", "dials.symmetry"]),
    ("cut_data.d_min", ["dials.estimate_resolution"]),
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


def is_bravais_summary(file_name):
    return file_name == "bravais_summary.json"


# files written with default names that never appear as output parameters,
# (test on the file name, program that wrote it)
IMPLICIT_OUTPUTS = [
    (is_bravais_setting, "dials.refine_bravais_settings"),
    (is_bravais_summary, "dials.refine_bravais_settings"),
]


def split_cmd_line(cmd_str):
    # every command in timing_data.json looks like:  prog  'arg1' 'arg2' ...
    cmd_str = cmd_str.strip()
    divide_pos = cmd_str.find("'")
    if divide_pos == -1:
        # command without arguments, e.g.: xia2.report
        return cmd_str, []

    exe_cmd = cmd_str[0:divide_pos].strip()
    par_lst = []
    for inner_cmd in cmd_str[divide_pos + 1:-1].split("' '"):
        if inner_cmd != "":
            par_lst.append(inner_cmd)

    return exe_cmd, par_lst


def classify_params(par_lst):
    # returns file names (no path) of possible inputs and of written outputs
    from_prev_lst = []
    for_next_lst = []
    skip_next = False
    for pos, single_par in enumerate(par_lst):
        if skip_next:
            skip_next = False

        elif (
            single_par in POSITIONAL_IN + POSITIONAL_OUT
            and pos + 1 < len(par_lst)
        ):
            file_name = reversed_find_str(str_in = par_lst[pos + 1])
            if single_par in POSITIONAL_OUT:
                for_next_lst.append(file_name)

            else:
                from_prev_lst.append(file_name)

            skip_next = True

        elif "=" in single_par:
            key = single_par[0:single_par.find("=")]
            value = single_par[single_par.find("=") + 1:]
            if value == "" or " " in value:
                # not a file, e.g.: dispersion.kernel_size=3 3
                continue

            file_name = reversed_find_str(str_in = value, lst_sep_lst = [os.sep])
            if is_output_key(key):
                # ignore non file outputs like output.project_name=AUTOMATIC
                if "." in file_name:
                    for_next_lst.append(file_name)

            else:
                from_prev_lst.append(file_name)

        else:
            from_prev_lst.append(reversed_find_str(str_in = single_par))

    return from_prev_lst, for_next_lst


def find_implicit_parent(file_name, prev_cmd_lst):
    for matches, exe_cmd in IMPLICIT_OUTPUTS:
        if matches(file_name):
            # most recent previous run of that program
            for prev_dict in reversed(prev_cmd_lst):
                if prev_dict['exe_cmd'] == exe_cmd:
                    return prev_dict['curr_poss']

    return None


def find_param_parent(single_par, prev_cmd_lst):
    for key, exe_cmd_lst in PARAM_FROM_PROGRAM:
        if single_par.startswith(key + "="):
            # most recent previous run of any of those programs
            for prev_dict in reversed(prev_cmd_lst):
                if prev_dict['exe_cmd'] in exe_cmd_lst:
                    return prev_dict['curr_poss']

    return None


def add_connection(parent_dict, child_dict, file_name):
    parent_poss = parent_dict['curr_poss']
    if parent_poss not in child_dict['parent_pos_lst']:
        child_dict['parent_pos_lst'].append(parent_poss)
        child_dict['files_from_parent_dict'][parent_poss] = []
        parent_dict['chidren_pos_lst'].append(child_dict['curr_poss'])

    if file_name not in child_dict['files_from_parent_dict'][parent_poss]:
        child_dict['files_from_parent_dict'][parent_poss].append(file_name)


def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    json_file = open(path_in, 'r', encoding="utf-8")
    entries_lst = json.load(json_file)
    json_file.close()

    list_of_commands = []
    curr_poss = 0
    for entry in entries_lst:
        exe_cmd, par_lst = split_cmd_line(entry["command"])
        if exe_cmd == 'dials.report':
            continue

        from_prev_lst, for_next_lst = classify_params(par_lst)
        cmd_dict = {
            'exe_cmd'                   :exe_cmd,
            'par_lst'                   :par_lst,
            'from_prev_lst'             :from_prev_lst,
            'for_next_lst'              :for_next_lst,
            'parent_pos_lst'            :[],
            'chidren_pos_lst'           :[],
            'files_from_parent_dict'    :{},
            'external_files_lst'        :[],
            'time_start'                :entry.get("time_start"),
            'time_end'                  :entry.get("time_end"),
            'curr_poss'                 :curr_poss,
        }
        curr_poss += 1
        list_of_commands.append(cmd_dict)

    # file name -> position of the most recent command that wrote it
    producer_of = {}
    for cur_num, curr_dict in enumerate(list_of_commands):
        for file_name in curr_dict['from_prev_lst']:
            if file_name in producer_of:
                parent_poss = producer_of[file_name]

            else:
                parent_poss = find_implicit_parent(
                    file_name, list_of_commands[0:cur_num]
                )

            if parent_poss is not None:
                add_connection(
                    list_of_commands[parent_poss], curr_dict, file_name
                )

            elif has_file_extension(file_name):
                curr_dict['external_files_lst'].append(file_name)

        for single_par in curr_dict['par_lst']:
            parent_poss = find_param_parent(
                single_par, list_of_commands[0:cur_num]
            )
            if parent_poss is not None:
                add_connection(
                    list_of_commands[parent_poss], curr_dict, single_par
                )

        if curr_dict['exe_cmd'] in USES_PREVIOUS_OUTPUT and cur_num > 0:
            add_connection(
                list_of_commands[cur_num - 1], curr_dict, "(implicit)"
            )

        for file_name in curr_dict['for_next_lst']:
            producer_of[file_name] = curr_dict['curr_poss']

    return list_of_commands


def short_label(label):
    # parameter values keep their name, files lose path and "key="
    for key, exe_cmd_lst in PARAM_FROM_PROGRAM:
        if label.startswith(key + "="):
            return label

    return reversed_find_str(str_in = label)


def print_graph_table(list_of_commands):
    # one row per connection, same format for every input file type
    fmt_str = "%-5s %-30s %-5s %-30s %s"
    print("\n", "=" * 90)
    print(fmt_str % ("from", "parent", "to", "child", "via"))
    print("-" * 90)
    for cmd_dict in list_of_commands:
        for parent_poss in sorted(cmd_dict['parent_pos_lst']):
            lbl_lst = []
            for label in cmd_dict['files_from_parent_dict'][parent_poss]:
                lbl_lst.append(short_label(label))

            print(fmt_str % (
                parent_poss, list_of_commands[parent_poss]['exe_cmd'],
                cmd_dict['curr_poss'], cmd_dict['exe_cmd'],
                ", ".join(sorted(lbl_lst)),
            ))

    print("=" * 90)


def print_commands(list_of_commands):
    print("\n", "=" * 90)
    t0 = 0.0
    if list_of_commands != [] and list_of_commands[0]['time_start'] is not None:
        t0 = list_of_commands[0]['time_start']

    for cmd_dict in list_of_commands:
        timing_str = ""
        if cmd_dict['time_start'] is not None and cmd_dict['time_end'] is not None:
            timing_str = "  (t=%.1fs, %.1fs)" % (
                cmd_dict['time_start'] - t0,
                cmd_dict['time_end'] - cmd_dict['time_start'],
            )




        '''
        print("\n[%d] %s%s" % (
            cmd_dict['curr_poss'], cmd_dict['exe_cmd'], timing_str
        ))
        for parent_poss in cmd_dict['parent_pos_lst']:
            print(
                "      <- [%d] %s: %s" % (
                    parent_poss, list_of_commands[parent_poss]['exe_cmd'],
                    ", ".join(cmd_dict['files_from_parent_dict'][parent_poss]),
                )
            )

        if cmd_dict['external_files_lst'] != []:
            print(
                "      <- external: %s" %
                ", ".join(cmd_dict['external_files_lst'])
            )

        if cmd_dict['for_next_lst'] != []:
            print("      -> %s" % ", ".join(cmd_dict['for_next_lst']))

        if cmd_dict['chidren_pos_lst'] != []:
            print("      children: %s" % cmd_dict['chidren_pos_lst'])
        '''





        '''

    for curr_dict in list_of_commands:
        for parent_poss in curr_dict['parent_pos_lst']:
            print(
                "connecting: ", parent_poss, " with ", curr_dict['curr_poss'],
                " via ", curr_dict['files_from_parent_dict'][parent_poss]
            )


        '''


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        arg_in = "timing_data.json"

    lst_cmd = get_list_of_commands(arg_in)
    print_graph_table(lst_cmd)


if __name__ == "__main__":
    main()
