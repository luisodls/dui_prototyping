'''
DUI's code generator from phil parameters

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


class gen_code(object):

    '''
    Source code generator in a non analytical way, this means this class does
    not read the Phil parameters, just generates the code after and before of
    the Phil dependent code, and writes into disc once passed the Phil
    dependent piece of code
    '''

    def __init__(self, qt_tool = "PyQt4"):

        self.src_code_1 = []
        self.src_code_1.append("import sys")

        if( qt_tool == "PyQt4" ):
            self.src_code_1.append("from PyQt4.QtGui import *")
            self.src_code_1.append("from PyQt4.QtCore import *")
            self.src_code_1.append("print \"using PyQt4\"")

        else:
            self.src_code_1.append("from PySide.QtGui import *")
            self.src_code_1.append("from PySide.QtCore import *")
            self.src_code_1.append("pyqtSignal = Signal")
            self.src_code_1.append("print \"using PySide\"")

        self.src_code_1.append("\n")

        self.src_code_1.append("class inner_widg( QWidget):")
        self.src_code_1.append("    item_changed = pyqtSignal()")
        self.src_code_1.append("    def __init__(self, parent = None):")
        self.src_code_1.append("        super(inner_widg, self).__init__(parent)")
        self.src_code_1.append("        self.super_parent = parent # reference across the hole GUI to MyMainDialog")
        self.src_code_1.append("        palette_scope = QPalette()")
        self.src_code_1.append("        palette_scope.setColor(QPalette.Foreground, QColor(85, 85, 85, 255))")
        self.src_code_1.append("        palette_object = QPalette()")
        self.src_code_1.append("        palette_object.setColor(QPalette.Foreground,Qt.black)")
        self.src_code_1.append("        bg_box =  QVBoxLayout(self)")
        self.src_code_1.append("\n")

        self.src_code_2 = []
        self.src_code_2.append(" ")
        self.src_code_2.append("        self.setLayout(bg_box)")
        self.src_code_2.append("        self.show()")
        self.src_code_2.append("\n")
        self.src_code_2.append("    def spnbox_changed(self, value):")
        self.src_code_2.append("        sender = self.sender()")
        self.src_code_2.append("        print \"sender =\", sender")
        self.src_code_2.append("        print \"spnbox_changed to:\",")
        self.src_code_2.append("        str_value = str(value)")
        self.src_code_2.append("        print value")
        #self.src_code_2.append("        print \"local_path =\",")
        self.src_code_2.append("        str_path = str(sender.local_path)")
        self.src_code_2.append("        self.super_parent.update_lin_txt(str_path, str_value, from_simple = False)")
        #self.src_code_2.append("        self.super_parent.update_lin_txt(sender.local_path, value)")
        self.src_code_2.append("\n")
        self.src_code_2.append("    def combobox_changed(self, value):")
        self.src_code_2.append("        sender = self.sender()")
        self.src_code_2.append("        print \"combobox_changed to: \",")
        self.src_code_2.append("        str_value = str(sender.tmp_lst[value])")
        self.src_code_2.append("        print str_value")
        #self.src_code_2.append("        print \"local_path =\",")
        self.src_code_2.append("        str_path = str(sender.local_path)")
        self.src_code_2.append("        print str_path")
        self.src_code_2.append("        self.super_parent.update_lin_txt(str_path, str_value, from_simple = False)")
        self.src_code_2.append("\n")
        self.src_code_2.append("class ParamMainWidget( QWidget):")
        self.src_code_2.append("    def __init__(self, parent = None):")
        self.src_code_2.append("        super(ParamMainWidget, self).__init__(parent)")
        self.src_code_2.append("        self.super_parent = parent # reference across the hole GUI to MyMainDialog")
        self.src_code_2.append("        self.scrollable_widget = inner_widg(self.super_parent)")
        self.src_code_2.append("        scrollArea = QScrollArea()")
        self.src_code_2.append("        scrollArea.setWidget(self.scrollable_widget)")
        self.src_code_2.append("        hbox =  QHBoxLayout()")
        self.src_code_2.append("        hbox.addWidget(scrollArea)")
        self.src_code_2.append("        self.setLayout(hbox)")
        self.src_code_2.append("        self.setWindowTitle('Phil dialog')")
        self.src_code_2.append("        self.show()")
        self.src_code_2.append("\n")
        self.src_code_2.append("    def to_be_caled_from_son_widg(self):")
        self.src_code_2.append("        print \"from parent parent_widget\"")
        self.src_code_2.append("\n")
        self.src_code_2.append("if __name__ == '__main__':")
        self.src_code_2.append("    app =  QApplication(sys.argv)")
        self.src_code_2.append("    ex = ParamMainWidget()")
        self.src_code_2.append("    sys.exit(app.exec_())")


    def write_file(self, to_insert = None, file_name = None):
        '''
        Writes code into a disc, but includes the "to_insert" list in the middle
        '''
        if( file_name == None ):
            file_name = "inner_mult_opt.py"
        else:
            file_name = file_name + ".py"

        myfile = open(file_name, "w")

        for line in self.src_code_1:
            myfile.write(line)
            myfile.write("\n")

        if( to_insert != None ):
            for line in to_insert:
                myfile.write(line)
                myfile.write("\n")

        for line in self.src_code_2:
            myfile.write(line)
            myfile.write("\n")

        myfile.close()

class ScopeData(object):
    '''
    class conceived to store only data related to the scope Phil object
    '''
    pass

class tree_2_lineal(object):

    '''
    Recursively navigates the Phil objects in a way that the final
    self.lst_obj is a lineal list without ramifications, this final list
    will be used by phil_list_2_disc() to generate runnable code
    '''

    def __init__(self, phl_obj):
        self.lst_obj = []
        self.deep_in_rec(phl_obj)

    def __call__(self):
        return self.lst_obj

    def deep_in_rec(self, phl_obj):

        for single_obj in phl_obj:
            if( single_obj.is_definition):
                self.lst_obj.append(single_obj)
                tmp_exercise = '''
                if( single_obj.name == "threshold_probability" ):
                    print "single_obj.name = threshold_probability"
                    tst_var = single_obj.extract()
                    print "single_obj.extract() = ", tst_var
                    tst_var_01 = float(tst_var)
                    print "type(tst_var_01) =", type(tst_var_01)
                    print "tst_var_01 =", tst_var_01
                    print "full_path =", single_obj.full_path()



                    print "\n"

                #print "single_obj.name =", single_obj.name
                #print "single_obj.extract() =", single_obj.extract()


                #print "\n"

                # end tmp
                '''
            elif( single_obj.is_scope ):
                #print "scope.name = ", single_obj.name
                scope_info = ScopeData()
                scope_info.name = str(single_obj.name)
                scope_info.f_path = str(single_obj.full_path())

                #print "scope_info.f_path =", scope_info.f_path
                scope_info.indent = scope_info.f_path.count('.')
                #print "scope_info.f_path.count('.') =", scope_info.indent

                self.lst_obj.append(scope_info)
                self.deep_in_rec(single_obj.objects)

            else:
                print "\n\n _____________ <<< WARNING neither definition or scope\n\n"


def phil_list_2_disc(lst_obj, file_name, qt_tool = "PyQt4"):

    '''
    generator of either PyQt4 or PySide GUI code that lets the user edit
    the Phil parameters, the code auto-generated here should be inserted
    between the s_code.src_code_1 and s_code.src_code_2 lists
    '''
    f_siz = "10"
    src_code_aut = []
    for nm, obj in enumerate(lst_obj):

        if( str(type(obj)) == "<class '__main__.ScopeData'>" ):
            my_str = "        label_" + str(nm) + " = QLabel(\"" + " " * int(obj.indent * 4)
            my_str += str(obj.name)  + "\")"
            src_code_aut.append(my_str)
            my_str = "        label_" + str(nm) + ".setPalette(palette_scope)"
            src_code_aut.append(my_str)
            my_str = "        label_" + str(nm) + ".setFont(QFont(\"Monospace\", 10, QFont.Bold))"
            #my_str = "        label_" + str(nm) + ".setFont(QFont(\"Monospace\", "
            #my_str += f_siz + ", QFont.Bold))"
            src_code_aut.append(my_str)
            my_str = "        bg_box.addWidget(label_" + str(nm) + ")"
            src_code_aut.append(my_str)

        else:
            multiple_index = False
            if(obj.type.phil_type == 'float' or
               obj.type.phil_type == 'int'   or
               obj.type.phil_type == 'str'   or
               obj.type.phil_type == 'bool'  or
               obj.type.phil_type == 'choice' ):

                h_box_name = "hbox_lay_" + str(obj.name) + "_" + str(nm)
                my_str = "        " + h_box_name + " =  QHBoxLayout()"
                src_code_aut.append(my_str)
                label_name = "label_" + str(obj.name) + "_" + str(nm)
                indent = str(obj.full_path()).count('.')
                my_str = "        " + label_name + " = QLabel(\""
                my_str += " " * indent * 4 + str(obj.name)  + "\")"
                src_code_aut.append(my_str)
                my_str = "        " + label_name + ".setPalette(palette_object)"
                src_code_aut.append(my_str)
                my_str = "        " + label_name + ".setFont(QFont(\"Monospace\", 10))"
                #my_str = "        " + label_name + ".setFont(QFont(\"Monospace\","
                #my_str += f_siz + ", QFont.Bold))"
                src_code_aut.append(my_str)
                my_str = "        " + h_box_name + ".addWidget(" + label_name + ")"
                src_code_aut.append(my_str)

                box_name = "box_" + str(obj.name) + "_" + str(nm)
                something_else = False
                if(obj.type.phil_type == 'float' or
                   obj.type.phil_type == 'int'   or
                   obj.type.phil_type == 'str'     ):
                    src_code_aut.append("")
                    if( obj.type.phil_type == 'float' ):
                        widget_type_str =" = QDoubleSpinBox()"

                    elif( obj.type.phil_type == 'int' ):
                        widget_type_str =" = QSpinBox()"

                    elif( obj.type.phil_type == 'str' ):
                        widget_type_str =" = QLineEdit()"

                    my_str = "        " + box_name + widget_type_str
                    src_code_aut.append(my_str)

                    if( obj.type.phil_type == 'int' or obj.type.phil_type == 'float'  ):
                        #print "str(obj.extract()) =", str(obj.extract())
                        #print "type(obj.extract()) =", type(obj.extract())
                        if( str(obj.extract()) == 'Auto' or str(obj.extract()) == 'None'):
                            print "TODO fix the libtbx.AutoType in double Phil parameter"

                        else:
                            my_str = "        " + box_name + ".setValue(" + str(obj.extract()) +")"
                            src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".local_path = \"" + str(obj.full_path()) +"\""
                    src_code_aut.append(my_str)

                    if( obj.type.phil_type == 'int' or obj.type.phil_type == 'float' ):
                        my_str = "        " + box_name + ".valueChanged.connect(self.spnbox_changed)"
                    else:
                        my_str = "        " + box_name + ".textChanged.connect(self.spnbox_changed)"

                    src_code_aut.append(my_str)

                elif( obj.type.phil_type == 'bool' ):

                    src_code_aut.append("")
                    my_str = "        " + box_name + " = QComboBox()"
                    src_code_aut.append(my_str)
                    my_str = "        " + box_name + ".local_path = \"" + str(obj.full_path()) +"\""
                    src_code_aut.append(my_str)
                    my_str = "        " + box_name + ".tmp_lst=[]"
                    src_code_aut.append(my_str)
                    my_str = "        " + box_name + ".tmp_lst.append(\"True\")"
                    src_code_aut.append(my_str)
                    my_str = "        " + box_name + ".tmp_lst.append(\"False\")"
                    src_code_aut.append(my_str)
                    my_str = "        for lst_itm in " + box_name + ".tmp_lst:"
                    src_code_aut.append(my_str)
                    my_str = "            " + box_name + ".addItem(lst_itm)"
                    src_code_aut.append(my_str)

                    if( str(obj.extract()) == "False" ):
                        my_str = "        " + box_name + ".setCurrentIndex(" + str(1) + ")"
                        src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".currentIndexChanged.connect(self.combobox_changed)"
                    src_code_aut.append(my_str)


                elif( obj.type.phil_type == 'choice' ):

                    src_code_aut.append("")
                    my_str = "        " + box_name + " = QComboBox()"
                    src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".local_path = \"" + str(obj.full_path()) +"\""
                    src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".tmp_lst=[]"
                    src_code_aut.append(my_str)

                    pos = 0
                    for nm, opt in enumerate(obj.words):
                        opt = str(opt)
                        if( opt[0] == "*" ):
                            opt = opt[1:]
                            pos = nm

                        my_str = "        " + box_name + ".tmp_lst.append(\"" + opt + "\")"
                        src_code_aut.append(my_str)

                    my_str = "        for lst_itm in " + box_name + ".tmp_lst:"
                    src_code_aut.append(my_str)
                    my_str = "            " + box_name + ".addItem(lst_itm)"
                    src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".setCurrentIndex(" + str(pos) + ")"
                    src_code_aut.append(my_str)

                    my_str = "        " + box_name + ".currentIndexChanged.connect(self.combobox_changed)"
                    src_code_aut.append(my_str)


            elif( obj.type.phil_type == 'ints' or obj.type.phil_type == 'floats' ):

                debug_code = '''
                print "\n\n"
                print "str(obj.type)=", str(obj.type)
                print "str(obj.type.phil_type)=", str(obj.type.phil_type)
                print "\n obj.full_path() =", obj.full_path()
                print "\n obj.type.size_max =", obj.type.size_max
                print "\n obj.type.size_min =", obj.type.size_min
                print "\n\n"
                '''


                if( obj.type.size_min >= 2 and obj.type.size_max <= 6 and
                    obj.type.size_max == obj.type.size_min and obj.type.size_max != None ):
                    h_box_name_lst = []
                    label_name_lst = []
                    box_name_lst = []
                    indent = str(obj.full_path()).count('.')

                    for indx in range(obj.type.size_max):
                        h_box_name_str = "hbox_lay_" + str(obj.name) + "_" + str(nm) + "_" + str(indx)
                        h_box_name_lst.append(h_box_name_str)
                        my_str = "        " + h_box_name_lst[indx] + " =  QHBoxLayout()"
                        src_code_aut.append(my_str)
                        label_name_str = "label_" + str(obj.name) + "_" + str(nm) + "_" + str(indx)
                        label_name_lst.append(label_name_str)
                        my_str = "        " + label_name_lst[indx] + " = QLabel(\""
                        my_str += " " * indent * 4 + str(obj.name) + "[" + str(indx + 1) + "]" + "\")"
                        src_code_aut.append(my_str)

                        my_str = "        " + label_name_lst[indx] + ".setPalette(palette_object)"
                        src_code_aut.append(my_str)
                        my_str = "        " + label_name_lst[indx] + ".setFont(QFont(\"Monospace\", 10))"
                        #my_str = "        " + label_name_lst[indx] + ".setFont(QFont(\"Monospace\","
                        #my_str += f_siz + ", QFont.Bold))"
                        src_code_aut.append(my_str)
                        my_str = "        " + h_box_name_lst[indx] + ".addWidget(" + label_name_lst[indx] + ")"
                        src_code_aut.append(my_str)
                        box_name_str = "box_" + str(obj.name) + "_" + str(nm) + "_" + str(indx)
                        box_name_lst.append(box_name_str)
                        if(obj.type.phil_type == 'ints'):
                            widget_type_str =" = QSpinBox()"
                        elif( obj.type.phil_type == 'floats' ):
                            widget_type_str =" = QDoubleSpinBox()"
                        my_str = "        " + box_name_lst[indx] + widget_type_str
                        src_code_aut.append(my_str)
                        my_str = "        " + box_name_lst[indx] + ".local_path = \"" + str(obj.full_path()) +"\""
                        src_code_aut.append(my_str)
                        my_str = "        #" + box_name_lst[indx] + ".valueChanged.connect(self.spnbox_changed)"
                        src_code_aut.append(my_str)
                    multiple_index = True


                else:
                    debug_code = '''
                    print
                    print "_______ << WARNING  obj.type.phil_type not previewed"
                    print "full_path =", obj.full_path()
                    print "obj.type.phil_type =", obj.type.phil_type
                    print "obj.type =", obj.type
                    print
                    '''
                    something_else = True

            else:

                print
                print "_____________________ << WARNING find something ELSE"
                print "_____________________ << full_path =", obj.full_path()
                print "_____________________ << obj.type.phil_type =", obj.type.phil_type
                print "_____________________ << obj.type =", obj.type
                print
                something_else = True

            if( something_else == False ):
                if(multiple_index == False):
                    my_str = "        " + h_box_name + ".addWidget(" + box_name + ")"
                    src_code_aut.append(my_str)
                    my_str = "        bg_box.addLayout(" + h_box_name + ")"
                    src_code_aut.append(my_str)

                else:
                    for indx in range(obj.type.size_max):
                        my_str = "        " + h_box_name_lst[indx] + ".addWidget(" + box_name_lst[indx] + ")"
                        src_code_aut.append(my_str)
                        my_str = "        bg_box.addLayout(" + h_box_name_lst[indx] + ")"
                        src_code_aut.append(my_str)

        src_code_aut.append("")

    s_code = gen_code(qt_tool)
    s_code.write_file(src_code_aut, file_name)


if( __name__ == "__main__"):

    from python_qt_bind import GuiBinding
    gui_lib = GuiBinding()
    print "using ", gui_lib.pyhon_binding
    qt_tool = gui_lib.pyhon_binding

    lst_phl_obj = []

    from dials.command_line.find_spots import phil_scope as phil_scope_find_spots
    lst_phl_obj.append([phil_scope_find_spots, "find_spots_mult_opt"])
    from dials.command_line.index import phil_scope as phil_scope_index
    lst_phl_obj.append([phil_scope_index, "index_mult_opt"])
    from dials.command_line.refine import phil_scope as phil_scope_refine
    lst_phl_obj.append([phil_scope_refine, "refine_mult_opt"])
    from dials.command_line.integrate import phil_scope as phil_scope_integrate
    lst_phl_obj.append([phil_scope_integrate, "integrate_mult_opt"])

    try:
        from dials.command_line.export import phil_scope as phil_scope_export
    except:
        from dials.command_line.export_mtz import phil_scope as phil_scope_export

    lst_phl_obj.append([phil_scope_export, "export_mult_opt"])


    for phl_obj in lst_phl_obj:
        lst_obj = tree_2_lineal(phl_obj[0].objects)
        phil_list_2_disc(lst_obj(), phl_obj[1], qt_tool)

        #print phl_obj[0].show()


