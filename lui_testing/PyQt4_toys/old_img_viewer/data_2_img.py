'''
Tools for converting from flex array to numpy bitmap

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

import sys, os
import numpy as np
from time import time as tm_now

from dials_viewer_ext import rgb_img
from dials.array_family import flex


try:
    from python_qt_bind import *

except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    print "    <<<   using PyQt4 (as exception)"



def gen_flex_arr(n_col = 800, n_row = 700):

    flex_data_out = flex.double(flex.grid(n_row, n_col),15)
    flex_mask_out = flex.double(flex.grid(n_row, n_col),0)

    for col in xrange(n_col):
        for row in xrange(n_row):
            flex_data_out[row, col] = col + row

    return flex_data_out, flex_mask_out


class img_w_cpp(object):
    def __init__(self):
        self.wx_bmp_arr = rgb_img()

    def __call__(self, flex_data_in, flex_mask_in, show_nums = False, i_min = -3.0, i_max = 200.0):

        err_code = self.wx_bmp_arr.set_min_max(i_min, i_max)
        #err_code = self.wx_bmp_arr.set_min_max(0.0, 1500.0)

        palette = "hot ascend"
        if palette == "black2white":
            palette_num = 1
        elif palette == "white2black":
            palette_num = 2
        elif palette == "hot ascend":
            palette_num = 3
        else: # assuming "hot descend"
            palette_num = 4

        img_array_tmp = self.wx_bmp_arr.gen_bmp(flex_data_in, flex_mask_in, show_nums, palette_num)

        np_img_array = img_array_tmp.as_numpy_array()

        height = np.size(np_img_array[:, 0:1, 0:1])
        width = np.size( np_img_array[0:1, :, 0:1])

        img_array = np.zeros([height, width, 4], dtype=np.uint8)

        #for some strange reason PyQt4 needs to use RGB as BGR
        img_array[:,:,0:1] = np_img_array[:,:,2:3]
        img_array[:,:,1:2] = np_img_array[:,:,1:2]
        img_array[:,:,2:3] = np_img_array[:,:,0:1]

        return img_array


if __name__ == "__main__":
    print "Hi"
    #building flex arrays
    flex_arr_2d, flex_mask_2d = gen_flex_arr()

    #building rgb_img
    arr_i = img_w_cpp()
    arr_i = arr_i(flex_arr_2d, flex_mask_2d)

    #converting to QImage
    print "before QImage generator"
    q_img = QImage(arr_i.data, np.size(arr_i[0:1, :, 0:1]),
                   np.size(arr_i[:, 0:1, 0:1]), QImage.Format_RGB32)
    print "after QImage generator"

    #building app with IMG
    app = QApplication([])
    pix = QPixmap.fromImage(q_img)
    lbl = QLabel()
    lbl.setPixmap(pix)
    lbl.show()

    app.exec_()

