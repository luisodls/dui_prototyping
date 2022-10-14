"""
DUI2's client's side contol and run utilities

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


from PySide2.QtCore import *
import requests, json, os, sys, zlib
from client.init_firts import ini_data

def get_optional_list(cmd_str):
    cmd = {"nod_lst":"", "cmd_lst":[cmd_str]}

    data_init = ini_data()
    uni_url = data_init.get_url()
    print("uni_url(get_optional_list) =", uni_url)

    lst_opt = json_data_request(uni_url, cmd)

    return lst_opt


def json_data_request(url, cmd):
    try:
        print("attempting to request to:", url, ", with:", cmd)
        req_get = requests.get(url, stream = True, params = cmd, timeout = 3)
        print("starting request")
        str_lst = ''
        line_str = ''
        json_out = ""
        times_loop = 10
        for count_times in range(times_loop):
            print("count_times =", count_times)
            tmp_dat = req_get.raw.readline()
            line_str = str(tmp_dat.decode('utf-8'))
            if line_str[-7:] == '/*EOF*/':
                print('/*EOF*/ received')
                break

            else:
                str_lst = line_str

            if count_times == times_loop - 1:
                print('to many "lines" in http response')
                json_out = None

        if json_out is not None:
            json_out = json.loads(str_lst)

    except ConnectionError:
        print(" ... Connection err catch  (json_data_request) ...")
        json_out = None

    except requests.exceptions.RequestException:
        print(" ... requests.exceptions.RequestException (json_data_request)")
        json_out = None

    return json_out


class Run_n_Output(QThread):
    new_line_out = Signal(str, int, str)
    first_line = Signal(int)
    about_to_end = Signal(int, bool)
    def __init__(self, request, do_pred_n_rept = False):
        super(Run_n_Output, self).__init__()
        self.request = request
        self.number = None
        self.do_predict_n_report = do_pred_n_rept

    def run(self):
        line_str = ''
        not_yet_read = True
        while True:
            tmp_dat = self.request.raw.readline()
            line_str = str(tmp_dat.decode('utf-8'))
            if line_str[-7:] == '/*EOF*/':
                #TODO: consider a different Signal to say finished
                print('>>  /*EOF*/  <<')
                break

            if not_yet_read:
                not_yet_read = False

                try:
                    nod_p_num = int(line_str.split("=")[1])
                    self.number = nod_p_num
                    print("\n QThread.number =", self.number)
                    self.first_line.emit(self.number)

                except IndexError:
                    print("\n *** Run_n_Output ... Index err catch *** \n")
                    not_yet_read = True

            else:
                self.new_line_out.emit(line_str, self.number, "Busy")

            self.usleep(1)

        self.about_to_end.emit(self.number, self.do_predict_n_report)

