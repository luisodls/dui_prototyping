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

    palette = "hot ascend"

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


qtCreatorFile = "test.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #print "dir(self.graphicsView_1)", dir(self.graphicsView_1)

        test1 = Test()
        test1.set_mask()
        test1.set_pars()

        a = test1.test_dispersion_debug()

        flex_final_mask = a.final_mask()

        np_global_mask = a.global_mask().as_numpy_array()
        np_cv_mask = a.cv_mask().as_numpy_array()
        np_value_mask = a.value_mask().as_numpy_array()
        np_mean = a.mean().as_numpy_array()

        flex_index_of_dispersion = a.index_of_dispersion()
        #building array
        arr_i = img_arr_n_cpp(flex_index_of_dispersion)

        #converting to QImage
        print "before QImage generator"
        q_img = QtGui.QImage(arr_i.data, np.size(arr_i[0:1, :, 0:1]),
                       np.size(arr_i[:, 0:1, 0:1]), QtGui.QImage.Format_RGB32)

        print "after QImage generator"

        #####################################################################
        '''
        print "building QImage in graphicsView_1 ... start"
        my_scene = QtGui.QGraphicsScene()
        self.graphicsView_1.setScene(my_scene)
        self.graphicsView_1.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        self.l_pixmap = QtGui.QPixmap.fromImage(q_img)
        my_scene.addPixmap(self.l_pixmap)
        print "building QImage in graphicsView_1 ... end"
        '''
        my_scene = QtGui.QGraphicsScene()
        self.graphicsView_1.setScene(my_scene)
        fileName = "../../../anaelu_git/forthon_01/miscellaneous/lena.jpeg"
        image = QtGui.QImage(fileName)
        self.l_pixmap = QtGui.QPixmap.fromImage(image)
        my_scene.addPixmap(self.l_pixmap)

        ####################################################################



        tmp_off = '''
        np_variance = a.variance().as_numpy_array()
        plt.imshow( np_variance , interpolation = "nearest" )
        plt.show()
        '''
        self.show()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())

