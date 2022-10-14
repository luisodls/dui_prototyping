"""
DUI's command simple stacked widgets

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import subprocess, psutil
import os, sys, shutil
import glob, json, time

from server.data_n_json import get_data_from_steps
from server.init_first import ini_data
from shared_modules import format_utils

def get_pair_list():
    return [
        ("d",       "display"                               ),
        ("h",       "history"                               ),
        ("gol",     "get_optional_command_list"             ),
        ("ip",      "dials.import"                          ),
        ("Aaa",    "dials.version"                            ),
    ]

def fix_alias(short_in):
    pair_list = get_pair_list()
    long_out = short_in
    for pair in pair_list:
        if pair[0] == short_in:
            print("replacing ", pair[0], " with ", pair[1])
            long_out = pair[1]

    return long_out


def unalias_full_cmd(lst_in):
    new_full_lst = []
    for inner_lst in lst_in:
        unalias_inner_lst = []
        for elem in inner_lst:
            unalias_inner_lst.append(fix_alias(elem))

        new_full_lst.append(unalias_inner_lst)

    return new_full_lst


def find_if_in_list(inner_command):
    print("find_if_in_list(multi_node)=", inner_command)
    pair_list = get_pair_list()
    found_command = False
    for pair in pair_list:
        if inner_command == pair[1]:
            found_command = True

    return found_command


def add_log_line(new_line, nod_req):
    if new_line[-1:] != "\n" and len(new_line) > 1:
        print("<<< adding \\n >>> to output line:", new_line)
        new_line += "\n"

    if nod_req is not None:
        try:
            nod_req.wfile.write(bytes(new_line , 'utf-8'))
            Error_Broken_Pipes = 0

        except BrokenPipeError:
            Error_Broken_Pipes = 1

    else:
        print(new_line[:-1])

    return Error_Broken_Pipes


class CmdNode(object):
    def __init__(self, parent_lst_in = None):

        data_init = ini_data()
        self.win_exe = data_init.get_win_exe()

        self.parent_node_lst = []

    def __call__(self, lst_in, req_obj = None):
        print("\n lst_in =", lst_in)

    def run_cmd(self, req_obj = None):
        self.nod_req = req_obj
        self.status = "Busy"
        print("self.full_cmd_lst =", self.full_cmd_lst)
        inner_lst = self.full_cmd_lst[-1]

        is_valid_command = find_if_in_list(inner_lst[0])
        print("is_valid_command =", is_valid_command)
        if is_valid_command:
            try:
                print("self.win_exe =", self.win_exe)
                if self.win_exe:
                    inner_lst[0] += ".exe"

                print("\n Running:", inner_lst, "\n")
                self.my_proc = subprocess.Popen(
                    inner_lst,
                    shell = False,
                    cwd = self._run_dir,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT,
                    universal_newlines = True
                )

            except FileNotFoundError:
                print(
                    "unable to run:", inner_lst[0],
                    " <<FileNotFound err catch >> "
                )
                self.my_proc = None
                return

        else:
            print(
                "\n\n" + "#" * 80 + "\n " + inner_lst[0] +
                " is NOT a Dials Command, NOT Running it \n" +
                "#" * 80 + "\n\n"
            )
            self.status = "Failed"
            return

        new_line = None
        log_line_lst = []
        self.log_file_path = self._run_dir + "/out.log"
        self.n_Broken_Pipes = 0
        if self.nod_req is not None:
            try:
                self.nod_req.send_response(201)
                self.nod_req.send_header('Content-type', 'text/plain')
                self.nod_req.end_headers()
                str_nod_num = "node.number=" + str(self.number) + "\n"
                self.nod_req.wfile.write(bytes(str_nod_num , 'utf-8'))

            except BrokenPipeError:
                print("\n << BrokenPipe err catch  >> while sending nod_num \n")

        while self.my_proc.poll() is None or new_line != '':
            new_line = self.my_proc.stdout.readline()
            self.n_Broken_Pipes += add_log_line(new_line, self.nod_req)
            log_line_lst.append(new_line[:-1])

        for inv_pos in range(1, len(log_line_lst)):
            if log_line_lst[-inv_pos] != '':
                log_line_lst = log_line_lst[0:-inv_pos]
                print("inv_pos =", inv_pos)
                break

        self.my_proc.stdout.close()
        if self.my_proc.poll() == 0:
            print("subprocess poll 0")

        else:
            print("\n  ***  err catch  *** \n\n poll =", self.my_proc.poll())
            self.status = "Failed"

        if self.status != "Failed":
            self.status = "Succeeded"

        lof_file = open(self.log_file_path, "w")
        for log_line in log_line_lst:
            wrstring = log_line + "\n"
            lof_file.write(wrstring)

        lof_file.close()

        if self.n_Broken_Pipes > 0:
            print("\n << BrokenPipe err catch >> while sending output \n")


class Runner(object):
    def __init__(self, recovery_data):
        self.tree_output = format_utils.TreeShow()
        if recovery_data == None:
            self.start_from_zero()

        else:
            self._recover_state(recovery_data)

    def start_from_zero(self):
        root_node = CmdNode()
        root_node.set_root()
        self.step_list = [root_node]
        self.bigger_lin = 0
        #self.lst_cmd_in = []

    def run_dials_command(self, cmd_dict, req_obj = None):
        unalias_cmd_lst = unalias_full_cmd(cmd_dict["cmd_lst"])
        print("\n cmd_lst: ", unalias_cmd_lst)

        tmp_parent_lst_in = []
        for lin2go in cmd_dict["nod_lst"]:
            for node in self.step_list:
                if node.number == lin2go:
                    tmp_parent_lst_in.append(node)

        node2run = self._create_step(tmp_parent_lst_in)
        for uni_cmd in unalias_cmd_lst:
            try:
                node2run(uni_cmd, req_obj)

            except UnboundLocalError:
                print("\n ***  err catch  *** \n wrong line \n not running")
                print("uni_cmd =", uni_cmd)

            self._save_state()

    def run_dui_command(self, cmd_dict, req_obj = None):
        unalias_cmd_lst = unalias_full_cmd(cmd_dict["cmd_lst"])

        if req_obj is not None:
            try:
                print("\n  Dui2 CMD( cmd_lst )= ", unalias_cmd_lst, "\n ")
                if unalias_cmd_lst == [['reset_graph']]:
                    req_obj.send_response(201)
                    req_obj.send_header('Content-type', 'text/plain')
                    req_obj.end_headers()
                    req_obj.wfile.write(bytes(
                        "err.code=0\n" , 'utf-8')
                    )
                    self.clear_run_dirs_n_reset()
                    req_obj.wfile.write(bytes(
                        "Reset tree ... Done\n" , 'utf-8')
                    )

                elif unalias_cmd_lst == [['run_predict_n_report']]:
                    req_obj.send_response(201)
                    req_obj.send_header('Content-type', 'text/plain')
                    req_obj.end_headers()
                    req_obj.wfile.write(bytes(
                        "err.code=0\n" , 'utf-8')
                    )
                    for lin2go in cmd_dict["nod_lst"]:
                        for node in self.step_list:
                            if node.number == lin2go:
                                self.run_predict_n_report(node, req_obj)

                    req_obj.wfile.write(bytes(
                        "run_predict_n_report ... Done\n" , 'utf-8')
                    )
            except BrokenPipeError:
                print(
                    "\n << BrokenPipe err catch >> while running Dui command\n"
                )



def str2dic(cmd_str):
    print("cmd_str =", cmd_str, "\n")

    cmd_dict = {"nod_lst":[],
                "cmd_lst":[]}

    lstpar = cmd_str.split(" ")
    for single_param in lstpar:
        try:
            cmd_dict["nod_lst"].append(int(single_param))

        except ValueError:
            break

    if len(cmd_dict["nod_lst"]) > 0:
        print("nod_lst=", cmd_dict["nod_lst"])

        new_par_str = ""
        for single_param in lstpar[len(cmd_dict["nod_lst"]):]:
            new_par_str += single_param + " "

        tmp_cmd_lst = new_par_str[0:-1].split(";")
        par_n_cmd_lst = []
        for single_command in tmp_cmd_lst:
            inner_lst = single_command.split(" ")
            par_n_cmd_lst.append(inner_lst)

    else:
        par_n_cmd_lst = [[cmd_str]]

    cmd_dict["cmd_lst"] = par_n_cmd_lst

    return cmd_dict


