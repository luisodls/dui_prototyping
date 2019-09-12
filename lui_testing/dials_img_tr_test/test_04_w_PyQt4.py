import sys
from PyQt4 import QtCore, QtGui, uic

from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory
#from scitbx.array_family import flex
import pickle

from dials_viewer_ext import rgb_img
from dials.array_family import flex

import numpy as np

class Test:
    def __init__(self):
        self.n_json_file_path = "/tmp/dui_run/dui_files/2_datablock.json"
        datablocks = DataBlockFactory.from_json_file(self.n_json_file_path)
        # TODO check length of datablock for safety
        datablock = datablocks[0]
        my_sweep = datablock.extract_sweeps()[0]
        self.image = my_sweep.get_raw_data(0)[0].as_double()

    def set_mask(self):
        experiments = ExperimentListFactory.from_json_file(
                        self.n_json_file_path, check_format=False
                    )

        self.imageset = experiments.imagesets()[0]
        mask_file = self.imageset.external_lookup.mask.filename

        pick_file = open(mask_file, "rb")
        mask_tup_obj = pickle.load(pick_file)
        pick_file.close()

        self.mask = mask_tup_obj[0]

    def set_pars(self):
        self.gain = 0.5
        self.size = (3, 3)
        self.nsig_b = 3
        self.nsig_s = 3
        self.global_threshold = 0
        self.min_count = 2

    def test_dispersion_debug(self):
        from dials.algorithms.image.threshold import DispersionThresholdDebug

        self.gain_map = flex.double(flex.grid(2527, 2463), self.gain)

        debug = DispersionThresholdDebug(
            self.image,
            self.mask,
            self.gain_map,
            self.size,
            self.nsig_b,
            self.nsig_s,
            self.global_threshold,
            self.min_count,
        )

        return debug


def img_arr_n_cpp(flex_data_in):

    wx_bmp_arr = rgb_img()
    flex_mask_in = flex.double(
            flex.grid(flex_data_in.all()[0], flex_data_in.all()[1]), 0
        )

    err_code = wx_bmp_arr.set_min_max(0.0, 28.0)

    palette = "white2black"

    if palette == "black2white":
        palette_num = 1
    elif palette == "white2black":
        palette_num = 2
    elif palette == "hot ascend":
        palette_num = 3
    else: # assuming "hot descend"
        palette_num = 4

    show_nums = False

    print "before c++"
    img_array_tmp = wx_bmp_arr.gen_bmp(flex_data_in, flex_mask_in, show_nums, palette_num)
    print "after c++"
    np_img_array = img_array_tmp.as_numpy_array()

    height = np.size(np_img_array[:, 0:1, 0:1])
    width = np.size( np_img_array[0:1, :, 0:1])

    img_array = np.zeros([height, width, 4], dtype=np.uint8)

    #for some strange reason PyQt4 needs to use RGB as BGR
    img_array[:,:,0:1] = np_img_array[:,:,2:3]
    img_array[:,:,1:2] = np_img_array[:,:,1:2]
    img_array[:,:,2:3] = np_img_array[:,:,0:1]

    print "end of np generator"

    return img_array

def get_pixmap_mono(flex_img_in):
    old_way = '''
    np_img = flex_img_in.as_numpy_array()
    q_img = QtGui.QImage(np.transpose(np_img),
                         np.size(np_img[0:1, :]),
                         np.size(np_img[:, 0:1]),
                         QtGui.QImage.Format_Mono)
    '''
    print dir(flex_img_in)

    np_img = flex_img_in.as_numpy_array()
    print "\n copy slise ... start"
    print "\n np.size(np_img) =", np.size(np_img)
    img_np = np.zeros([2527, 2463], dtype=np.double)
    img_np[:,:] = np_img[:,:]
    double_img = flex.double(img_np)
    print "\n copy slise ... end \n"

    arr_img = img_arr_n_cpp(double_img)
    q_img = QtGui.QImage(arr_img.data, np.size(arr_img[0:1, :, 0:1]),
                   np.size(arr_img[:, 0:1, 0:1]), QtGui.QImage.Format_RGB32)

    tmp_pixmap = QtGui.QPixmap.fromImage(q_img)

    #return QtGui.QPixmap.fromImage(q_img)
    return tmp_pixmap


qtCreatorFile = "test02.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Scene01(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(Scene01, self).__init__()
        print("TsT")


    def dragLeaveEvent(self, event):
        print("dragLeaveEvent(event)")

    def dragEnterEvent(self, event):
        print("dragEnterEvent(event)")

    def dragMoveEvent(self, event):
        print("dragMoveEvent(event)")

    def dropEvent(self, event):
        print("dropEvent(event)")

    def focusInEvent(self, event):
        print("focusInEvent(event)")

    def focusOutEvent(self, event):
        print("focusOutEvent(event)")

    def keyPressEvent(self, event):
        print("keyPressEvent(event)")

    def keyReleaseEvent(self, event):
        print("keyReleaseEvent(event)")

    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent(event)")

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent(event)")

    def mousePressEvent(self, event):
        print("mousePressEvent(event)")

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent(event)")

    def wheelEvent(self, event):
        print("wheelEvent(event)")


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #print "dir(self.graphicsView_1)", dir(self.graphicsView_1)

        test1 = Test()
        test1.set_mask()
        test1.set_pars()

        self.debug_data = test1.test_dispersion_debug()

        self.my_scene_1 = Scene01(self)
        #self.graphicsView_1.setMouseTracking(True)

        self.graphicsView_1.setScene(self.my_scene_1)
        self.graphicsView_1.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        #print "\n dir(self.my_scene_1)", dir(self.my_scene_1), "\n"
        #print "\n dir(self.graphicsView_1)", dir(self.graphicsView_1), "\n"

        self.my_scene_2 = QtGui.QGraphicsScene()
        self.graphicsView_2.setScene(self.my_scene_2)
        self.graphicsView_2.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        self.my_scene_3 = QtGui.QGraphicsScene()
        self.graphicsView_3.setScene(self.my_scene_3)
        self.graphicsView_3.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        self.pushButton_1.clicked.connect(self.set_img_1)
        self.pushButton_2.clicked.connect(self.set_img_2)
        self.pushButton_3.clicked.connect(self.set_img_3)

        self.pushButton_4.clicked.connect(self.set_img_4)
        self.pushButton_5.clicked.connect(self.set_img_5)
        self.pushButton_6.clicked.connect(self.set_img_6)
        self.setWindowTitle('Testing')
        self.show()

    def set_img_1(self):
        print "Hi ..."
        flex_index_of_dispersion = self.debug_data.index_of_dispersion()
        #building array
        arr_i = img_arr_n_cpp(flex_index_of_dispersion)
        #converting to QImage
        q_img = QtGui.QImage(arr_i.data, np.size(arr_i[0:1, :, 0:1]),
                       np.size(arr_i[:, 0:1, 0:1]), QtGui.QImage.Format_RGB32)

        tmp_pixmap = QtGui.QPixmap.fromImage(q_img)
        try:
            self.my_scene_1.clear()
            self.my_scene_1.addPixmap(tmp_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"

    def set_img_2(self):
        print "Hi ..."
        flex_global_mask = self.debug_data.global_mask()
        new_pixmap = get_pixmap_mono(flex_global_mask)
        try:
            self.my_scene_2.clear()
            self.my_scene_2.addPixmap(new_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"

        ###########################################################################
    def set_img_3(self):
        print "set_img_3"
        ######################################################################################
        flex_mean = self.debug_data.mean()
        print "type(flex_mean)", type(flex_mean)
        ######################################################################################
        '''
        print "Hi ..."
        flex_mean = self.debug_data.global_mask()
        new_pixmap = get_pixmap_mono(flex_mean)
        try:
            self.my_scene_2.clear()
            self.my_scene_2.addPixmap(new_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"
        '''

    def set_img_4(self):
        print "set_img_4"
        ######################################################################################
        flex_value_mask = self.debug_data.value_mask()
        print "type(flex_value_mask)", type(flex_value_mask)
        ######################################################################################
        '''
        print "Hi ..."
        flex_mean = self.debug_data.global_mask()
        new_pixmap = get_pixmap_mono(flex_mean)
        try:
            self.my_scene_2.clear()
            self.my_scene_2.addPixmap(new_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"
        '''

    def set_img_5(self):
        print "set_img_5"
        ######################################################################################
        flex_cv_mask = self.debug_data.cv_mask()
        print "type(flex_cv_mask)", type(flex_cv_mask)
        ######################################################################################
        '''
        print "Hi ..."
        flex_mean = self.debug_data.global_mask()
        new_pixmap = get_pixmap_mono(flex_mean)
        try:
            self.my_scene_2.clear()
            self.my_scene_2.addPixmap(new_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"
        '''

    def set_img_6(self):
        print "set_img_6"
        ######################################################################################
        flex_final_mask = self.debug_data.final_mask()
        print "type(flex_final_mask)", type(flex_final_mask)
        ######################################################################################
        '''
        print "Hi ..."
        flex_mean = self.debug_data.global_mask()
        new_pixmap = get_pixmap_mono(flex_mean)
        try:
            self.my_scene_2.clear()
            self.my_scene_2.addPixmap(new_pixmap)

        except:
            print "failed to refresh"

        print "... Bye"
        '''



        old_one = '''
    def set_img_3(self):
        print "Hi ..."
        fileName = "/home/ufn91840/M_Pics/chihuahua.png"
        image = QtGui.QImage(fileName)
        tmp_pixmap = QtGui.QPixmap.fromImage(image)
        self.my_scene_3.addPixmap(tmp_pixmap)
        print "... Bye"
        '''


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())


