import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

import numpy as np
import json

from dials_viewer_ext import rgb_img
from dials.array_family import flex

class img_w_cpp:
    def __init__(self):
        self.wx_bmp_arr = rgb_img()

    def __call__(
        self,
        np_2d_img,
        np_2d_mask = None,
        show_nums=False,
        i_min=-3.0,
        i_max=200.0,
        palette="heat",
    ):

        self.wx_bmp_arr.set_min_max(i_min, i_max)

        if palette == "invert":
            palette_num = 1
        elif palette == "grayscale":
            palette_num = 2
        elif palette == "heat invert":
            palette_num = 3
        else:  # assuming "hot descend"
            palette_num = 4

        #######################################################

        xmax = np_2d_img.shape[1]
        ymax = np_2d_img.shape[0]

        if np_2d_mask is None:
            np_2d_mask = np.zeros((ymax, xmax), "double")

        transposed_data = np.zeros((ymax, xmax), "double")
        transposed_mask = np.zeros((ymax, xmax), "double")

        transposed_data[:, :] = np_2d_img
        transposed_mask[:, :] = np_2d_mask

        flex_data_in = flex.double(transposed_data)
        flex_mask_in = flex.double(transposed_mask)

        #######################################################

        img_array_tmp = self.wx_bmp_arr.gen_bmp(
            flex_data_in, flex_mask_in, show_nums, palette_num
        )

        np_img_array = img_array_tmp.as_numpy_array()

        height = np.size(np_img_array[:, 0:1, 0:1])
        width = np.size(np_img_array[0:1, :, 0:1])

        img_array = np.zeros([height, width, 4], dtype=np.uint8)

        # for some strange reason PyQt4 needs to use RGB as BGR
        img_array[:, :, 0:1] = np_img_array[:, :, 2:3]
        img_array[:, :, 1:2] = np_img_array[:, :, 1:2]
        img_array[:, :, 2:3] = np_img_array[:, :, 0:1]

        return img_array



def load_json_w_str():

    with open("arr_img.json") as json_file:
        arr_dic = json.load(json_file)

    d1 = arr_dic["d1"]
    d2 = arr_dic["d2"]
    str_data = arr_dic["str_data"]
    print("d1, d2 =", d1, d2)
    #print("str_data =", str_data)
    arr_1d = np.fromstring(str_data, dtype = float, sep = ',')
    np_array_out = arr_1d.reshape(d1, d2)
    #print("np_array_out =\n", np_array_out)

    conv_img = img_w_cpp()
    rgb_np_img = conv_img(np_2d_img = np_array_out)

    return rgb_np_img


class Form(QObject):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("my_win.ui")
        self.my_scene_1 = QGraphicsScene()
        self.window.graphicsView.setScene(self.my_scene_1)
        self.window.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.window.LoadButton.clicked.connect(self.btn_clk)
        self.window.show()

    def btn_clk(self):
        print("self.btn_clk start")
        np_array_img = load_json_w_str()
        print("here 1")
        q_img = QImage(
            np_array_img.data,
            np.size(np_array_img[0:1, :, 0:1]),
            np.size(np_array_img[:, 0:1, 0:1]),
            QImage.Format_RGB32,
        )
        print("here 2")
        self.pixmap = QPixmap(q_img)

        print("here 3")
        self.my_scene_1.addPixmap(self.pixmap)
        print("here 4")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

