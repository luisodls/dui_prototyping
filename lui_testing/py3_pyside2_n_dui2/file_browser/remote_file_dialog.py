"""
DUI2's remote file browser

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

import sys, os, json, logging, requests
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

def sort_dict_list(lst_in):
    list_size = len(lst_in)
    for i in range(list_size):
        min_index = i
        for j in range(i + 1, list_size):
            if lst_in[min_index]["name"] > lst_in[j]["name"]:
                min_index = j

        lst_in[i], lst_in[min_index] = lst_in[min_index], lst_in[i]

    return lst_in


class MyDirView_list(QListWidget):
    file_clickled = Signal(dict)
    def __init__(self, parent = None):
        super(MyDirView_list, self).__init__(parent)
        self.itemClicked.connect(self.someting_click)
        self.itemDoubleClicked.connect(self.someting_2_clicks)
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)
        DirPixMapi = getattr(QStyle, 'SP_DirIcon')
        FilePixMapi = getattr(QStyle, 'SP_FileIcon')
        self.icon_dict = {
            "True":self.style().standardIcon(DirPixMapi),
            "False":self.style().standardIcon(FilePixMapi)
        }

    def enter_list(self, lst_in):
        lst_in = sort_dict_list(lst_in)
        self.items_list = []
        for single_file in lst_in:
            tst_item = QListWidgetItem(single_file["name"])
            tst_item.f_isdir = single_file["isdir"]
            tst_item.f_path = str(single_file["path"])
            tst_item.setIcon(self.icon_dict[str(tst_item.f_isdir)])
            self.items_list.append(tst_item)

        self.clear()
        for tst_item in self.items_list:
            self.addItem(tst_item)

    def someting_click(self, item):
        self.file_clickled.emit({"isdir":item.f_isdir, "path":item.f_path})

    def someting_2_clicks(self, item):
        self.someting_click(item)


class PathButtons(QWidget):
    up_dir_clickled = Signal(str)
    def __init__(self, parent = None):
        super(PathButtons, self).__init__()
        self.main_h_lay = QHBoxLayout()
        self.lst_butt = []
        self.main_h_lay.addStretch()
        self.setLayout(self.main_h_lay)

    def update_list(self, new_list):
        for single_widget in self.lst_butt:
            single_widget.deleteLater()
            self.main_h_lay.removeWidget(single_widget)

        self.lst_butt = []
        path_str = ""
        for dir_name in new_list:
            new_butt = QPushButton(dir_name)
            path_str += dir_name + os.sep
            new_butt.own_path = path_str
            new_butt.clicked.connect(self.dir_clicked)
            self.lst_butt.append(new_butt)
            self.main_h_lay.addWidget(new_butt)

            new_lab = QLabel(" > ")
            self.lst_butt.append(new_lab)
            self.main_h_lay.addWidget(new_lab)


    def dir_clicked(self):
        next_path = str(self.sender().own_path)
        self.up_dir_clickled.emit(next_path)


class PathBar(QWidget):
    clicked_up_dir = Signal(str)
    def __init__(self, parent = None):
        super(PathBar, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.path_buttons = PathButtons(self)
        self.path_buttons.up_dir_clickled.connect(self.up_dir)
        self.scroll_path = QScrollArea()
        self.scroll_path.setWidgetResizable(True)
        self.scroll_path.setWidget(self.path_buttons)
        self.hscrollbar = self.scroll_path.horizontalScrollBar()
        self.hscrollbar.rangeChanged.connect(self.scroll_2_right)
        mainLayout.addWidget(self.scroll_path)
        self.setLayout(mainLayout)
        self.setFixedHeight(self.height() * 2.6)

    def scroll_2_right(self, minimum, maximum):
        self.hscrollbar.setValue(maximum)

    def update_list(self, new_list):
        self.path_buttons.update_list(new_list)

    def up_dir(self, next_path):
        self.clicked_up_dir.emit(next_path)


class OpenFileDialog(QDialog):
    def __init__(self, parent=None):
        super(OpenFileDialog, self).__init__(parent)
        self.setWindowTitle("Open IMGs")
        mainLayout = QVBoxLayout()
        self.show_hidden_check = QCheckBox("Show Hidden Files")
        self.show_hidden_check.setChecked(False)
        self.show_hidden_check.stateChanged.connect(self.refresh_content)
        hi_h_layout = QHBoxLayout()
        hi_h_layout.addStretch()
        hi_h_layout.addWidget(self.show_hidden_check)
        mainLayout.addLayout(hi_h_layout)

        self.path_bar = PathBar(self)
        self.path_bar.clicked_up_dir.connect(self.build_content)
        mainLayout.addWidget(self.path_bar)

        self.lst_vw =  MyDirView_list()
        self.ini_path = "/home/"
        self.build_content(self.ini_path)
        self.lst_vw.file_clickled.connect(self.fill_clik)
        mainLayout.addWidget(self.lst_vw)

        low_h_layout = QHBoxLayout()
        low_h_layout.addStretch()

        OpenButton = QPushButton(" Open ")
        OpenButton.clicked.connect(self.open_file)
        low_h_layout.addWidget(OpenButton)

        CancelButton = QPushButton(" Cancel ")
        CancelButton.clicked.connect(self.cancel_opp)
        low_h_layout.addWidget(CancelButton)

        mainLayout.addLayout(low_h_layout)
        self.setLayout(mainLayout)

    def build_content(self, path_in):
        self.curr_path = path_in
        self.refresh_content()

    def build_paren_list(self):
        print("self.curr_path", self.curr_path)
        parents_list = [self.ini_path[:-1]]
        rest_of_path = self.curr_path[len(self.ini_path):]
        print("rest_of_path = ", rest_of_path, "\n")
        for single_dir in rest_of_path.split(os.sep)[:-1]:
            parents_list.append(single_dir)

        self.path_bar.update_list(parents_list)

    def refresh_content(self):
        show_hidden = self.show_hidden_check.isChecked()
        self.current_file = None
        self.build_paren_list()

        os_listdir = os.listdir(self.curr_path)
        lst_dir = []
        for nm, f_name in enumerate(os_listdir):
            if f_name[0] != "." or show_hidden:
                f_path = self.curr_path + f_name
                f_isdir = os.path.isdir(f_path)
                lst_dir.append(
                    {
                        "name": f_name, "isdir":  f_isdir, "path": f_path
                    }
                )

        self.lst_vw.enter_list(lst_dir)

    def fill_clik(self, fl_dic):
        print("path = ", fl_dic["path"])
        if fl_dic == self.current_file:
            self.open_file()

        self.current_file = fl_dic

    def open_file(self):
        try:
            if self.current_file["isdir"]:
                self.build_content(self.current_file["path"] + os.sep)

            else:
                print("Opened: ", self.current_file["path"])

        except TypeError:
            print("no file selected yet")

    def cancel_opp(self):
        print("Cancel clicked")


uni_url = 'http://127.0.0.1:45678/'
#uni_url = 'http://127.0.0.1:45679/'
#uni_url = 'http://supercomputo.cimav.edu.mx:45678/'

def do_request(cmd_in):
    try:
        [parent, cmd] = cmd_in.split(",")

    except ValueError:
        [parent, cmd] = ["", cmd_in]

    full_cmd = {"nod_lst":[parent], "cmd_lst":[cmd]}

    req_get = requests.get(uni_url, stream = True, params = full_cmd)

    while True:
        tmp_dat = req_get.raw.readline()
        line_str = str(tmp_dat.decode('utf-8'))

        if '/*EOF*/' in line_str:
            print('/*EOF*/ received')
            break

        else:
            str_lst = str(line_str[:-1])

    lst_out = json.loads(str_lst)
    return lst_out


if __name__ == "__main__":
    to_try_later = '''
    app = QApplication(sys.argv)
    F_diag = OpenFileDialog()
    F_diag.show()
    sys.exit(F_diag.exec_())
    #########################################################################################
    '''

    cmd_in = "get_dir_ls /home/lui/"
    print("\n testing (", cmd_in, " )command\n")
    str_lst = do_request(cmd_in)
    for one_str in str_lst:
        print("str_lst =", str_lst)

