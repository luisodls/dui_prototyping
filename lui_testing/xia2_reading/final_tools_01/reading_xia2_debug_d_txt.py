import sys, os
from graph_common import (
    reversed_find_str, is_output_key, has_file_extension,
    is_bravais_setting, find_implicit_parent, find_param_parent,
    print_graph_table, export_reusable_graph_list, is_dials_command,
    find_work_dirs, POSITIONAL_IN, POSITIONAL_OUT
)


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


def add_connection(parent_dict, child_dict, file_name):
    parent_poss = parent_dict['curr_poss']
    if parent_poss not in child_dict['parent_pos_lst']:
        child_dict['parent_pos_lst'].append(parent_poss)
        child_dict['files_from_parent_dict'][parent_poss] = []
        parent_dict['chidren_pos_lst'].append(child_dict['curr_poss'])

    child_dict['files_from_parent_dict'][parent_poss].append(file_name)


def get_list_of_commands(path_in):
    print("file 2 read = ", path_in)
    log_file = open(path_in, 'r', encoding="utf-8")
    lines_str = log_file.readlines()
    log_file.close()
    list_of_commands = []
    curr_poss = 0
    for position, single_line in enumerate(lines_str):
        if single_line[0:15] == "# command line:":
            new_cmd_str = lines_str[position + 1][1:]
            exe_cmd, full_cmd_lst = split_cmd_line(new_cmd_str)

            if not is_dials_command(exe_cmd) or exe_cmd == 'dials.report':
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

            cmd_dict = {
                'full_cmd_lst'              :full_cmd_lst,
                'exe_cmd'                   :exe_cmd,
                'par_lst'                   :full_cmd_lst[1:],
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

    find_work_dirs(list_of_commands)

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

            add_connection(list_of_commands[parent_poss], curr_dict, file_name)

        for single_par in curr_dict['tuning_params_lst']:
            parent_poss = find_param_parent(
                single_par, list_of_commands[0:cur_num]
            )
            if parent_poss is not None:
                add_connection(
                    list_of_commands[parent_poss], curr_dict, single_par
                )

        for file_name in (
            curr_dict['expt_for_next_lst'] +
            curr_dict['refl_for_next_lst'] +
            curr_dict['another_for_next_lst']
        ):
            producer_of[file_name] = curr_dict['curr_poss']

    return list_of_commands


def main():
    try:
        arg_in = sys.argv[1]

    except IndexError:
        print("Enter path of file to read ... /xia2-debug.txt")
        lst_cmd = []

    else:
        lst_cmd = get_list_of_commands(arg_in)
        print_graph_table(lst_cmd)

        export_reusable_graph_list(lst_cmd)


if __name__ == "__main__":
    main()
