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

    def draw_4_me(self, lst_out):
        print("lst_out(draw_4_me) =", json.loads(lst_out))
        self.addRect(
            10, 10,
            10, 10,
            self.gray_pen, self.first_gray_brush
        )
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
        self.tree_scene.draw_4_me(lst_out)

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

