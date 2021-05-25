import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools

import numpy as np
import json

from dials_viewer_ext import rgb_img
from dials.array_family import flex


class np2bmp_heat(object):
    def __init__(self):

        self.red_byte = np.empty( (255 * 3), 'int')
        self.green_byte = np.empty( (255 * 3), 'int')
        self.blue_byte = np.empty( (255 * 3), 'int')

        for i in range(255):
            self.red_byte[i] = i
            self.green_byte[i + 255] = i
            self.blue_byte[i + 255 * 2 ] = i

        self.red_byte[255:255 * 3] = 255
        self.green_byte[0:255] = 0
        self.green_byte[255 * 2 : 255 * 3] = 255
        self.blue_byte[0:255 * 2] = 0

        self.blue_byte[764] = 255
        self.red_byte[764] = 255
        self.green_byte[764] = 255


    def img_2d_rgb(self, data2d = None, invert = False,
                   sqrt_scale = False, i_min_max = [None, None]):

        data2d_ini = np.copy(data2d)
        if(sqrt_scale == True):
            prev_max = data2d_ini.max()
            prev_min = data2d_ini.min()
            for x in np.nditer(
                data2d_ini[:,:], op_flags=['readwrite'],
                flags=['external_loop']
            ):
                x[...] = np.sqrt(x[...])

            if i_min_max[0] > 0:
                i_min_max[0] = np.sqrt(i_min_max[0])

            if i_min_max[1] > 0:
                i_min_max[1] = np.sqrt(i_min_max[1])

        data2d_min = data2d_ini.min()
        data2d_max = data2d_ini.max()

        self.local_min_max = [float(data2d_min), float(data2d_max)]
        if(i_min_max == [None, None]):
            print("no max and min provided")

        else:
            if(i_min_max[0] < data2d_min):
                data2d_min = i_min_max[0]

            if(i_min_max[1] > data2d_max):
                data2d_max = i_min_max[1]

        self.width = np.size( data2d_ini[0:1, :] )
        self.height = np.size( data2d_ini[:, 0:1] )

        data2d_pos = data2d_ini[:,:] - data2d_min + 1.0
        data2d_pos_max = data2d_pos.max()

        calc_pos_max = data2d_max - data2d_min + 1.0
        if(calc_pos_max > data2d_pos_max):
            data2d_pos_max = calc_pos_max

        div_scale = 764.0 / data2d_pos_max

        data2d_scale = np.multiply(data2d_pos, div_scale)


        if(invert == True):
            for x in np.nditer(
                data2d_scale[:,:], op_flags=['readwrite'],
                flags=['external_loop']
            ):
                x[...] = 764.0 - x[...]

        #img_array = np.empty( (self.height ,self.width, 3),'uint8')
        img_array = np.zeros([self.height, self.width, 4], dtype=np.uint8)

        img_array_r = np.empty( (self.height, self.width), 'int')
        img_array_g = np.empty( (self.height, self.width), 'int')
        img_array_b = np.empty( (self.height, self.width), 'int')

        scaled_i = np.empty( (self.height, self.width), 'int')
        scaled_i[:,:] = data2d_scale[:,:]

        img_array_r[:,:] = scaled_i[:,:]
        for x in np.nditer(
            img_array_r[:,:], op_flags=['readwrite'],
            flags=['external_loop']
        ):
            x[...] = self.red_byte[x]

        img_array_g[:,:] = scaled_i[:,:]
        for x in np.nditer(
            img_array_g[:,:], op_flags=['readwrite'],
            flags=['external_loop']
        ):
            x[...] = self.green_byte[x]

        img_array_b[:,:] = scaled_i[:,:]
        for x in np.nditer(
            img_array_b[:,:], op_flags=['readwrite'],
            flags=['external_loop']
        ):
            x[...] = self.blue_byte[x]

        img_array[:, :, 3] = 255
        img_array[:, :, 2] = img_array_r[:,:] #Blue
        img_array[:, :, 1] = img_array_g[:,:] #Green
        img_array[:, :, 0] = img_array_b[:,:] #Red

        return img_array



def load_json_w_str():

    with open("arr_img.json") as json_file:
        arr_dic = json.load(json_file)

    d1 = arr_dic["d1"]
    d2 = arr_dic["d2"]
    str_data = arr_dic["str_data"]
    print("d1, d2 =", d1, d2)
    arr_1d = np.fromstring(str_data, dtype = float, sep = ',')
    np_array_out = arr_1d.reshape(d1, d2)

    return np_array_out


class Form(QObject):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("my_win.ui")
        self.my_scene_1 = QGraphicsScene()
        self.bmp_heat = np2bmp_heat()
        self.window.graphicsView.setScene(self.my_scene_1)
        self.window.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.window.LoadButton.clicked.connect(self.btn_clk)
        self.window.show()

    def btn_clk(self):
        print("self.btn_clk start")

        np_array_img = load_json_w_str()

        rgb_np = self.bmp_heat.img_2d_rgb(
            data2d = np_array_img, invert = False,
            sqrt_scale = False, i_min_max = [None, None]
        )

        q_img = QImage(
            rgb_np.data,
            np.size(rgb_np[0:1, :, 0:1]),
            np.size(rgb_np[:, 0:1, 0:1]),
            QImage.Format_ARGB32
        )
        tmp_pixmap = QPixmap.fromImage(q_img)
        self.my_scene_1.addPixmap(tmp_pixmap)

        print("self.btn_clk end")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

