'''
DIALS User Interface

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
'''
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.




from __future__ import division
type_from_sh_cli = '''
export BOOST_ADAPTBX_FPE_DEFAULT=1
export BOOST_ADAPTBX_SIGNALS_DEFAULT=1
'''
or_here_in_python_code = '''
# LIBTBX_PRE_DISPATCHER_INCLUDE_SH export BOOST_ADAPTBX_FPE_DEFAULT=1
# LIBTBX_PRE_DISPATCHER_INCLUDE_SH export BOOST_ADAPTBX_SIGNALS_DEFAULT=1
'''
'''
# FIXME Copied from dials.index.py. This is needed here because scipy needs to
# be imported before cctbx otherwise there will be a segmentation fault. This
# should be fixed in dials.index so that we don't need to import here.
try:
  # try importing scipy.linalg before any cctbx modules, otherwise we
  # sometimes get a segmentation fault/core dump if it is imported after
  # scipy.linalg is a dependency of sklearn.cluster.DBSCAN
  import scipy.linalg # import dependency
except ImportError, e:
  pass
'''
from stacked_widgets import ImportPage, FindspotsParameterWidget,\
                            IndexParameterWidget, ReIndexWidget, \
                            RefineParameterWidget, IntegrateParameterWidget,\
                            ExportParameterWidget, \
                            QtCore, QtGui, QtWebKit

import subprocess
import sys
import os

from cli_interactions import TextBrows, MyQProcess, CmdLine

class MyMainDialog(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainDialog, self).__init__(parent)

        my_dui_path = os.environ["DUI_PATH"]
        dials_logo_path = my_dui_path + "/../dui/resources/DIALS_Logo_icon_ish.png"
        self.setWindowIcon(QtGui.QIcon(dials_logo_path))

        self.contentsWidget = QtGui.QListWidget()
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        #self.contentsWidget.setIconSize(QtCore.QSize(96, 84))
        self.contentsWidget.setIconSize(QtCore.QSize(56, 44))
        self.contentsWidget.setMovement(QtGui.QListView.Static)

        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setMinimumWidth(118)
        self.contentsWidget.setMinimumHeight(524)
        self.contentsWidget.setSpacing(12)

        self.pagesWidget = QtGui.QStackedWidget(self)
        self.widget_list = []
        self.widget_list.append(ImportPage(self))
        self.widget_list.append(FindspotsParameterWidget(self))
        self.widget_list.append(IndexParameterWidget(self))

        self.widget_list.append(ReIndexWidget(self))

        self.widget_list.append(RefineParameterWidget(self))
        self.widget_list.append(IntegrateParameterWidget(self))
        self.widget_list.append(ExportParameterWidget(self))


        #self.pagesWidget.setMaximumWidth(650)

        for widg in self.widget_list:
            self.pagesWidget.addWidget(widg)

        self.go_underline = "\n           "
        self.default_go_label = " \n Go" + self.go_underline

        self.Go_button = QtGui.QPushButton(self.default_go_label)
        self.Go_button.setFont(QtGui.QFont("Monospace", 14, QtGui.QFont.Bold))

        self.Go_button.setSizePolicy( QtGui.QSizePolicy.Maximum , QtGui.QSizePolicy.Maximum )

        self.createIcons()
        self.contentsWidget.setCurrentRow(0)

        self.Go_button.clicked.connect(self.onGoBtn)


        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        exec_layout = QtGui.QHBoxLayout()

        self.gui_line_edit = CmdLine()
        exec_layout.addWidget(self.gui_line_edit)

        exec_layout.addWidget(self.Go_button)

        mainLayout = QtGui.QVBoxLayout()

        self.multi_line_txt = TextBrows()

        mainLayout.addLayout(horizontalLayout)
        mainLayout.addLayout(exec_layout)

        main_widget = QtGui.QWidget()
        main_widget.setLayout(mainLayout)
        self.resize(1200, 900)
        self.setCentralWidget(main_widget)

        try:
            self.qProcess  = MyQProcess(self)
            self.qProcess.setProcessChannelMode(QtCore.QProcess.SeparateChannels);
            print "MyQProcess() ready"
        except:
            print "Failed to create MyQProcess()"


    def update_lin_txt(self, param_name = None, param_value = None,
                       from_simple = None, new_line = None):

        if(param_name != None):
            found_param = False
            for local_pname in self.param_changed_lst:
                if( local_pname[0] == param_name ):
                    local_pname[1] = param_value
                    found_param = True

            if(found_param == False):
                self.param_changed_lst.append([param_name,param_value])

            my_cli_string = self.cli_str

            for local_pname in self.param_changed_lst:
                my_cli_string += ( " " + str(local_pname[0]) +
                                   "=" + str(local_pname[1]) )

            first_attempt_to_connect_simple_with_advances_parameters = '''
            if( from_simple != None ):
                self.curr_indx = self.pagesWidget.currentIndex()
                self.widget_list[self.curr_indx].update_parms(from_simple)
            else:
                print "I don t know where the signal came from"
            '''

        elif( new_line != None ):
            my_cli_string = new_line

        self.gui_line_edit.set_text(my_cli_string)


    def createIcons(self):
        for widget in self.widget_list:
            page_n_button = QtGui.QListWidgetItem(self.contentsWidget)
            page_n_button.setIcon(QtGui.QIcon(widget.logo_path))
            page_n_button.setText(widget.button_label)
            page_n_button.setTextAlignment(QtCore.Qt.AlignHCenter)
            page_n_button.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)


    def changePage(self, current, previous):

        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))
        self.curr_indx = self.pagesWidget.currentIndex()
        self.cli_str = self.widget_list[self.curr_indx].cmd_lin_default

        try:
            self.gui_line_edit.set_text(str(self.cli_str))
        except:
            pass

        self.param_changed_lst = []


    def onGoBtn(self, event = None):
        print "\n from onGoBtn: event =", event, "\n"


        if( event != True ):
            print "\n onGoBtn \n", "event =", event
            self.curr_indx = self.pagesWidget.currentIndex()
            self.rung_indx = self.curr_indx
            self.widget_list[self.rung_indx].second_go_flag = True


        if( self.qProcess.run_stat == False):
            self.shell_str_to_run = str(self.gui_line_edit.get_text())

            print "CLI to Run =", self.shell_str_to_run

            self.qProcess.start(self.shell_str_to_run)
            self.gui_line_edit.set_text(str("Running >> {" + self.shell_str_to_run + " }" ))

        else:
            print "self.qProcess.run_stat != False"



    def on_started(self):
        tmp_txt = "\n" + " Starting " + self.go_underline
        self.Go_button.setText(tmp_txt)
        str_to_print = str("\nRunning >> { " + self.shell_str_to_run + " }" )

        #self.rung_indx = self.pagesWidget.currentIndex()
        self.widget_list[self.rung_indx].multi_line_txt.append_green(str_to_print)

    def update_go_txt(self, txt_str):
        tmp_txt = "\n" + txt_str + self.go_underline
        self.Go_button.setText(tmp_txt)

    def on_finished(self):

        self.Go_button.setText("Updating")
        self.gui_line_edit.set_text(str(""))

        print "Done CLI"

        if( self.rung_indx != 0 ):
            try:
                do_update = self.widget_list[self.rung_indx].run_extra_code()
                if( do_update == True ):
                    #self.widget_list[self.rung_indx].analyse_out_img.update_me()
                    self.widget_list[self.rung_indx].report_out_widg.update_me()
            except:
                print "WARNING  >>> got stuck in latest step after running CLI"
        self.Go_button.setText(self.default_go_label)


    def append_line(self, line_out, err_out = False):

        if( not err_out ):
            self.widget_list[self.rung_indx].multi_line_txt.append_black(line_out)

        else:
            print "Error detected"
            err_line = "ERROR: { \n" + line_out + " } "
            self.widget_list[self.rung_indx].multi_line_txt.append_red(err_line)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    print "screen (width, height) =", width, height

    dialog = MyMainDialog()
    dialog.show()
    sys.exit(app.exec_())

