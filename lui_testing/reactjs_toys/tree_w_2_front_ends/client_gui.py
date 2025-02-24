import sys, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

tree_data_str = []
tree_data_map = []

def build_tree_recr(pos_num, my_lst, indent = 1, parent_row = 0):
    step = my_lst[pos_num]
    stp_suss = ""
    tmp_off = '''
    if step["success"] == True:
        stp_suss = " T "

    elif step["success"] == False:
        stp_suss = " F "

    else:
        stp_suss = " N "
    '''

    str_lin_num = str(step["lin_num"])
    stp_prn = stp_suss + "  " + str_lin_num + "     " * indent + " └──"
    stp_cmd = str(step["command"])
    stp_prn = stp_prn + stp_cmd

    step_map = {
      "command": stp_cmd, "lin_num": step["lin_num"], "success": stp_suss,
      "indent":indent, "here":step["here"], "my_row":len(tree_data_map),
      "parent_row":parent_row
    }
    tree_data_str.append(stp_prn)
    tree_data_map.append(step_map)

    try:
        for new_pos in step["nxt"]:
            build_tree_recr(new_pos, my_lst, indent + 1, step_map["my_row"])

    except:
        print("last indent =", indent)


class TreeDirScene(QGraphicsScene):
    tmp_off = '''
    node_clicked_w_left = Signal(int)
    node_clicked_w_right = Signal(int)
    hide_clicked = Signal(int)
    '''
    def __init__(self, parent = None):
        super(TreeDirScene, self).__init__(parent)
        self.setFont(QFont("Courier"))
        fm_rect = QFontMetrics(self.font()).boundingRect("W")
        self.f_width = fm_rect.width()
        self.f_height = fm_rect.height()
        self.gray_pen = QPen(
            Qt.gray, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
        )
        self.first_gray_brush = QBrush(Qt.gray, Qt.SolidPattern)
        self.arrow_blue_pen = QPen(
                Qt.blue, 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
            )
    def draw_4_me(self, lst_out):
        #print("lst_out(draw_4_me) =", json.loads(lst_out))
        my_lst = lst_out['Answer']
        tot_hey = len(my_lst)
        print("tot_hey =", tot_hey)

        self.clear()

        for row_num in range(0, tot_hey + 1, 2):
            print("row_num =", row_num)
            x_ini = -5
            y_ini = row_num * self.f_height
            y_end = (row_num + 1) * self.f_height
            self.addRect(
                x_ini, y_ini,
                380, self.f_height,
                self.gray_pen, self.first_gray_brush
            )
            self.addLine(x_ini, y_ini, x_ini + 50, y_end, self.arrow_blue_pen)

        self.update()

        build_tree_recr(0, my_lst, 1, 0);
        for single_line in tree_data_str:
            print(single_line)


class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.window.Button4Get.clicked.connect(self.clicked_4_get)
        self.window.Button4Post.clicked.connect(self.clicked_4_post)
        self.window.EditPostRequestLine.textChanged.connect(self.new_req_txt)
        self.req_qr = ""
        self.tree_scene = TreeDirScene(self)
        self.window.TreeGraphicsView.setScene(self.tree_scene)
        self.window.show()

    def clicked_4_get(self):
        print("clicked_4_get")
        full_cmd = {"message":self.req_qr}
        req_get = requests.get(
            "http://127.0.0.1:45678", params = full_cmd
        )
        lst_out = req_get.content
        self.tree_scene.draw_4_me(json.loads(lst_out))

    def clicked_4_post(self):
        print("time to do a http(Post) request with:", self.req_qr)

        full_cmd = {"message":self.req_qr}
        req_post = requests.post(
            "http://127.0.0.1:45678", data = json.dumps(full_cmd)
        )
        lst_out = req_post.content
        print("lst_out =", json.loads(lst_out))

    def new_req_txt(self, new_txt):
        self.req_qr = str(new_txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

