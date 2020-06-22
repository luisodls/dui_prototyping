
import os, sys
import time, json


from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
from PySide2.QtGui import *

import out_utils
from gui_utils import TreeGitScene, TreeDirScene

lst_nodes = [{'lin_num': 0, 'status': 'Succeeded', 'cmd2show': ['Root'], 'child_node_lst': [1, 12, 13, 14, 15], 'parent_node_lst': []}, {'lin_num': 1, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [2, 5], 'parent_node_lst': [0]}, {'lin_num': 2, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [3, 6], 'parent_node_lst': [1]}, {'lin_num': 3, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [4, 7], 'parent_node_lst': [2]}, {'lin_num': 4, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [8], 'parent_node_lst': [3]}, {'lin_num': 5, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [9, 10, 11], 'parent_node_lst': [1]}, {'lin_num': 6, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [9, 10, 11], 'parent_node_lst': [2]}, {'lin_num': 7, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [9, 10, 11], 'parent_node_lst': [3]}, {'lin_num': 8, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [9, 10, 11], 'parent_node_lst': [4]}, {'lin_num': 9, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [5, 6, 7, 8]}, {'lin_num': 10, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [5, 6, 7, 8]}, {'lin_num': 11, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [5, 6, 7, 8]}, {'lin_num': 12, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [16, 17, 18], 'parent_node_lst': [0]}, {'lin_num': 13, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [16, 17, 18], 'parent_node_lst': [0]}, {'lin_num': 14, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [16, 17, 18], 'parent_node_lst': [0]}, {'lin_num': 15, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [16, 17, 18], 'parent_node_lst': [0]}, {'lin_num': 16, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [12, 13, 14, 15]}, {'lin_num': 17, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [12, 13, 14, 15]}, {'lin_num': 18, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [19, 20, 21], 'parent_node_lst': [12, 13, 14, 15]}, {'lin_num': 19, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [22], 'parent_node_lst': [18]}, {'lin_num': 20, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [23], 'parent_node_lst': [18]}, {'lin_num': 21, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [24], 'parent_node_lst': [18]}, {'lin_num': 22, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [25], 'parent_node_lst': [19]}, {'lin_num': 23, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [26], 'parent_node_lst': [20]}, {'lin_num': 24, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [27], 'parent_node_lst': [21]}, {'lin_num': 25, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [28, 29, 33], 'parent_node_lst': [22]}, {'lin_num': 26, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [28, 30, 33], 'parent_node_lst': [23]}, {'lin_num': 27, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [28, 31, 33], 'parent_node_lst': [24]}, {'lin_num': 28, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [25, 26, 27]}, {'lin_num': 29, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [32], 'parent_node_lst': [25]}, {'lin_num': 30, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [32], 'parent_node_lst': [26]}, {'lin_num': 31, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [32], 'parent_node_lst': [27]}, {'lin_num': 32, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [29, 30, 31]}, {'lin_num': 33, 'status': 'Succeeded', 'cmd2show': ['ls'], 'child_node_lst': [], 'parent_node_lst': [25, 26, 27]}]


class MainObject(QObject):
    def __init__(self, parent = None):
        super(MainObject, self).__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        ui_path += os.sep + "main_dui.ui"
        self.window = QtUiTools.QUiLoader().load(ui_path)

        self.tree_obj = out_utils.TreeShow()

        self.my_scene1 = TreeGitScene(self)
        self.window.gitView.setScene(self.my_scene1)
        self.my_scene1.draw_inner_graph([])


        self.my_scene2 = TreeDirScene(self)
        self.window.treeView.setScene(self.my_scene2)
        self.my_scene2.draw_tree_graph([])


        self.window.show()
        self.my_scene1.clear()
        self.my_scene1.draw_inner_graph(lst_nodes)
        self.my_scene1.update()


        lst_str = self.tree_obj(lst_nod = lst_nodes)
        lst_2d_dat = self.tree_obj.get_tree_data()
        self.my_scene2.clear()
        self.my_scene2.draw_tree_graph(lst_2d_dat)
        self.my_scene2.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_obj = MainObject()
    sys.exit(app.exec_())


