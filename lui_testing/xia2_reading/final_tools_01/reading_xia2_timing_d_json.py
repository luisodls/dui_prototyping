import sys, os, json
from graph_common import (
    reversed_find_str, is_output_key, has_file_extension,
    is_bravais_setting, find_implicit_parent, find_param_parent,
    print_graph_table, export_reusable_graph_list, is_dials_command,
    find_work_dirs, POSITIONAL_IN, POSITIONAL_OUT,
)


# commands without arguments that work on what the previous command wrote,
# e.g.: convert-mtz-sca converts the .mtz just written by dials.export/merge
USES_PREVIOUS_OUTPUT = ["convert-mtz-sca"]


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


def find_expt_n_refl(file_lst):

    # picks the .expt and the .refl files, needed by export_reusable_graph_list
    expt_lst = []
    refl_lst = []
    for file_name in file_lst:
        if file_name.endswith(".expt"):
            expt_lst.append(file_name)

        elif file_name.endswith(".refl"):
            refl_lst.append(file_name)

    return expt_lst, refl_lst


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
        if not is_dials_command(exe_cmd) or exe_cmd == 'dials.report':
            continue

        from_prev_lst, for_next_lst = classify_params(par_lst)
        expt_from_prev_lst, refl_from_prev_lst = find_expt_n_refl(from_prev_lst)
        expt_for_next_lst, refl_for_next_lst = find_expt_n_refl(for_next_lst)
        cmd_dict = {
            'exe_cmd'                   :exe_cmd,
            'par_lst'                   :par_lst,
            'from_prev_lst'             :from_prev_lst,
            'for_next_lst'              :for_next_lst,
            'expt_from_prev_lst'        :expt_from_prev_lst,
            'refl_from_prev_lst'        :refl_from_prev_lst,
            'expt_for_next_lst'         :expt_for_next_lst,
            'refl_for_next_lst'         :refl_for_next_lst,
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


    find_work_dirs(list_of_commands, os.path.dirname(os.path.abspath(path_in)))

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


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        arg_in = "timing_data.json"

    lst_cmd = get_list_of_commands(arg_in)
    print_graph_table(lst_cmd)
    export_reusable_graph_list(lst_cmd)


if __name__ == "__main__":
    main()
