import sys, requests, json
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

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
        tot_hey = len(lst_out['Answer'])
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

        data2remove = '''
lst_out(draw_4_me) = {'Answer': [{'lin_num': 0, 'command': 'None', 'prev_step': None, 'nxt': [1, 8], 'here': False}, {'lin_num': 1, 'command': 'a', 'prev_step': 0, 'nxt': [2, 6, 7], 'here': False}, {'lin_num': 2, 'command': 'a', 'prev_step': 1, 'nxt': [3, 4, 5], 'here': False}, {'lin_num': 3, 'command': 'a', 'prev_step': 2, 'nxt': [10], 'here': False}, {'lin_num': 4, 'command': 'b', 'prev_step': 2, 'nxt': [], 'here': False}, {'lin_num': 5, 'command': 'b', 'prev_step': 2, 'nxt': [], 'here': False}, {'lin_num': 6, 'command': 'c', 'prev_step': 1, 'nxt': [9], 'here': False}, {'lin_num': 7, 'command': 'c', 'prev_step': 1, 'nxt': [], 'here': False}, {'lin_num': 8, 'command': 'xxx', 'prev_step': 0, 'nxt': [], 'here': False}, {'lin_num': 9, 'command': 'y', 'prev_step': 6, 'nxt': [], 'here': False}, {'lin_num': 10, 'command': 'z', 'prev_step': 3, 'nxt': [], 'here': True}]}
        '''
        self.update()


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

