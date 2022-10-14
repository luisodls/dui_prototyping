"""
DUI2's Main window << Object >> on client side

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

import os, sys, requests

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

from client.exec_utils import (
    get_optional_list, build_advanced_params_widget, json_data_request,
    Run_n_Output, CommandParamControl
)

from client.init_firts import ini_data

from client.simpler_param_widgets import RootWidg
from client.simpler_param_widgets import ImportWidget
from client.simpler_param_widgets import MaskWidget
from client.simpler_param_widgets import ExportWidget
from client.simpler_param_widgets import OptionalWidget
from client.simpler_param_widgets import (
    FindspotsSimplerParameterTab, IndexSimplerParamTab,
    RefineBravaiSimplerParamTab, RefineSimplerParamTab,
    IntegrateSimplerParamTab, SymmetrySimplerParamTab,
    ScaleSimplerParamTab, CombineExperimentSimplerParamTab
)


class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)
        self.parent_app = parent
        self.ui_dir_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = self.ui_dir_path + os.sep + "dui_client.ui"
        print("ui_path =", ui_path)

        self.window = QtUiTools.QUiLoader().load(ui_path)
        self.window.setWindowTitle("CCP4 DUI2")

        dui2_icon = QIcon()
        st_icon_path = self.ui_dir_path + os.sep + "resources" \
            + os.sep + "DIALS_Logo_smaller_centred.png"
        dui2_icon.addFile(st_icon_path, mode = QIcon.Normal)
        self.window.setWindowIcon(dui2_icon)

        data_init = ini_data()
        self.uni_url = data_init.get_url()



        self.opt_cmd_lst = get_optional_list("get_optional_command_list")





    def request_launch(self):
        cmd_lst = self.new_node.get_full_command_list()
        lst_of_node_str = self.new_node.parent_node_lst
        cmd = {'nod_lst': lst_of_node_str, 'cmd_lst': cmd_lst}
        print("cmd =", cmd)
        self.window.incoming_text.clear()
        self.window.incoming_text.setTextColor(self.log_show.green_color)

        do_pred_n_rept = bool(
            self.window.RunPedictAndReportCheckBox.checkState()
        )

        try:
            new_req_post = requests.post(
                self.uni_url, stream = True, data = cmd
            )
            new_thrd = Run_n_Output(new_req_post, do_pred_n_rept)
            new_thrd.new_line_out.connect(self.log_show.add_line)
            new_thrd.first_line.connect(self.line_n1_in)
            new_thrd.about_to_end.connect(self.thread_to_end)
            new_thrd.finished.connect(self.request_display)
            new_thrd.finished.connect(self.check_nxt_btn)
            new_thrd.finished.connect(self.refresh_output)
            new_thrd.start()
            self.thrd_lst.append(new_thrd)

        except requests.exceptions.RequestException:
            print("something went wrong with the request of Dials comand")
            #TODO: put inside this << except >> some way to kill << new_thrd >>

    def line_n1_in(self, nod_num_in):
        self.request_display()
        print("line_n1_in(nod_num_in) = ", nod_num_in)
        #TODO: consider if this line goes in << request_launch >>
        self.new_node = None

    def req_stop(self):
        print("req_stop")
        nod_lst = [str(self.curr_nod_num)]
        print("\n nod_lst", nod_lst)
        cmd = {"nod_lst":nod_lst, "cmd_lst":["stop"]}
        print("cmd =", cmd)
        try:
            lst_params = json_data_request(self.uni_url, cmd)

        except requests.exceptions.RequestException:
            print(
                "something went wrong with the Stop request"
            )

    def reset_graph_triggered(self):
        print("reset_graph_triggered(QObject)")
        cmd = {"nod_lst":"", "cmd_lst":["reset_graph"]}
        print("cmd =", cmd)
        try:
            self.do_load_html.reset_lst_html()
            new_req_post = requests.post(
                self.uni_url, stream = True, data = cmd
            )
            new_thrd = Run_n_Output(new_req_post)
            new_thrd.first_line.connect(self.respose_n1_from_reset)
            new_thrd.finished.connect(self.request_display)
            new_thrd.start()
            self.thrd_lst.append(new_thrd)

        except requests.exceptions.RequestException:
            print(
                "something went wrong with the << reset_graph >> request"
            )
            #TODO: put inside this << except >> some way to kill << new_thrd >>

    def respose_n1_from_reset(self, line):
        print("respose_from_reset(err code):", line)

    def thread_to_end(self, nod_num_out, do_pred_n_rept):
        print("thread_to_end(QObject)")
        if do_pred_n_rept:
            cmd = {"nod_lst":[nod_num_out], "cmd_lst":["run_predict_n_report"]}
            print("cmd =", cmd)
            try:
                self.do_load_html.reset_lst_html()
                new_req_post = requests.post(
                    self.uni_url, stream = True, data = cmd
                )
                new_thrd = Run_n_Output(new_req_post)
                new_thrd.finished.connect(self.refresh_output)
                new_thrd.start()
                self.thrd_lst.append(new_thrd)

            except requests.exceptions.RequestException:
                print(
                    "something went wrong with the << reset_graph >> request"
                )
                #TODO: put inside this << except >> some way
                #TODO: to kill << new_thrd >>


