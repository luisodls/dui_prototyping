import sys
from PyQt4 import QtCore, QtGui, uic

from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory
from scitbx.array_family import flex
import pickle

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

        np_final_mask = a.final_mask().as_numpy_array()
        np_global_mask = a.global_mask().as_numpy_array()
        np_cv_mask = a.cv_mask().as_numpy_array()
        np_value_mask = a.value_mask().as_numpy_array()
        np_index_of_dispersion = a.index_of_dispersion().as_numpy_array()
        np_mean = a.mean().as_numpy_array()

        tmp_off = '''
        np_variance = a.variance().as_numpy_array()
        plt.imshow( np_variance , interpolation = "nearest" )
        plt.show()
        '''



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

