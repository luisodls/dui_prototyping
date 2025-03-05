import sys, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

def draw_quadratic_bezier_3_points(
        scene_obj, p1x, p1y, p2x, p2y, p3x, p3y, lin_pen
):
    curv_p1x = p1x
    curv_p1y = p1y
    curv_p2x = p2x
    curv_p2y = p2y
    curv_p3x = p3x
    curv_p3y = p3y

    n_points = 10

    dx12 = (curv_p2x - curv_p1x) / n_points
    dx23 = (curv_p3x - curv_p2x) / n_points

    dy12 = (curv_p2y - curv_p1y) / n_points
    dy23 = (curv_p3y - curv_p2y) / n_points

    for pos in range(n_points + 1):
        x1 = curv_p1x + dx12 * float(pos)
        y1 = curv_p1y + dy12 * float(pos)
        x2 = curv_p2x + dx23 * float(pos)
        y2 = curv_p2y + dy23 * float(pos)

        dx1 = (x2 - x1) / n_points
        dy1 = (y2 - y1) / n_points

        gx1 = x1 + dx1 * float(pos)
        gy1 = y1 + dy1 * float(pos)

        if pos > 0:
            scene_obj.addLine(x, y, gx1, gy1, lin_pen)

        x = gx1
        y = gy1



class TreeDirScene(QGraphicsScene):
    tmp_off = '''
    node_clicked_w_left = Signal(int)
    node_clicked_w_right = Signal(int)
    hide_clicked = Signal(int)
    '''
    def __init__(self, parent = None):
        super(TreeDirScene, self).__init__(parent)
        self.setFont(QFont("Mono"))
        fm_rect = QFontMetrics(self.font()).boundingRect("W")
        self.f_width = fm_rect.width()
        self.f_height = fm_rect.height()

        self.row_height = self.f_height * 1.5

        print("self.f_height =", self.f_height)

        self.gray_pen = QPen(
            Qt.gray, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
        )

        self.first_gray_brush = QBrush(Qt.lightGray, Qt.SolidPattern)
        self.another_gray_brush = QBrush(Qt.white, Qt.SolidPattern)
        self.arrow_blue_pen = QPen(
                Qt.blue, 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
            )
        self.invisible_brush = QBrush(Qt.white, Qt.NoBrush)
        self.rectang_pen = QPen(
            Qt.white, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
        )
        self.font_brush = QBrush(Qt.blue, Qt.SolidPattern)

    def build_tree_recr(self, pos_num, my_lst, indent = 1, parent_row = 0):
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
        if indent > self.max_indent:
            self.max_indent = int(indent)

        str_lin_num = str(step["lin_num"])
        stp_prn = stp_suss + "  " + str_lin_num + "     " * indent + " └──"
        stp_cmd = str(step["command"])
        stp_prn = stp_prn + stp_cmd

        step_map = {
            "command": stp_cmd, "lin_num": step["lin_num"],
            "success": stp_suss, "indent":indent, "here":step["here"], "my_row":len(self.tree_data_map), "parent_row":parent_row
        }

        self.tree_data_str.append(stp_prn)
        self.tree_data_map.append(step_map)

        try:
            print("step =", step)
            for new_pos in step["nxt"]:
                self.build_tree_recr(new_pos, my_lst, indent + 1, step_map["my_row"])

        except:
            print("last indent =", indent)


    def draw_4_me(self, lst_out):
        my_lst = lst_out['Answer']
        tot_hey = len(my_lst)
        print("tot_hey =", tot_hey)

        self.tree_data_str = []
        self.tree_data_map = []
        self.max_indent = 0
        self.build_tree_recr(0, my_lst, 1, 0);
        print("self.max_indent =", self.max_indent)

        self.clear()
        x_ini = -5
        box_wit = self.max_indent * 140
        self.addRect(
            x_ini - 10, -10,
            box_wit + 20, self.row_height * (tot_hey  + 2),
            self.gray_pen, self.first_gray_brush
        )

        for row_num in range(0, tot_hey + 1, 2):
            print("row_num =", row_num)
            y_ini = row_num * self.row_height
            y_end = (row_num + 1) * self.row_height
            self.addRect(
                x_ini, y_ini,
                box_wit, self.row_height,
                self.rectang_pen, self.another_gray_brush
            )

        x_scale = 25
        y_scale = self.row_height
        for ste_pos in self.tree_data_map[1:]:
            x_ini_vezier = (ste_pos["indent"] * 2.5 - 1.5) * x_scale
            x_end_vezier = (ste_pos["indent"] * 2.5) * x_scale

            y_ini_vezier = (ste_pos["my_row"] + 0.9) * y_scale
            y_end_vezier = (ste_pos["my_row"] + 1.5) * y_scale

            draw_quadratic_bezier_3_points(
                self,
                p1x = x_ini_vezier, p1y = y_ini_vezier,
                p2x = x_ini_vezier, p2y = y_end_vezier,
                p3x = x_end_vezier, p3y = y_end_vezier,
                lin_pen = self.arrow_blue_pen
            )

            self.addLine(
                x_ini_vezier, y_ini_vezier,
                x_ini_vezier, (ste_pos["parent_row"] + 2.0) * y_scale,
                self.arrow_blue_pen
            )

        for ste_pos in self.tree_data_map:
            x_text_corner = (ste_pos["indent"] * 2.5 + 0.3) * x_scale
            y_text_corner = (ste_pos["my_row"] + 1.1) * y_scale
            cmd_text = self.addSimpleText(str(ste_pos["command"]))
            cmd_text.setPos(x_text_corner, y_text_corner)
            cmd_text.setBrush(self.font_brush)

        self.update()

        for single_line in self.tree_data_str:
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

