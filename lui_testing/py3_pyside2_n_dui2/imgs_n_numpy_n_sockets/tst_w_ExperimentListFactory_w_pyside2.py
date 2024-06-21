#from dials.array_family import flex

from dxtbx.model.experiment_list import ExperimentListFactory
from dxtbx.flumpy import to_numpy
import time

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class LoadImages(QThread):
    image_loaded = Signal(str)
    def __init__(self, path_in = None, img_num = None):
        super(LoadImages, self).__init__()
        self.exp_path = path_in
        self.img_num = img_num

    def run(self):

        print("\n on_sweep_img_num =", self.img_num)
        experiments = get_experiments(self.exp_path)
        my_sweep = experiments.imagesets()[0]
        raw_dat = my_sweep.get_raw_data(self.img_num)
        data_xy_flex = raw_dat[0].as_double()
        np_arr2 = to_numpy(data_xy_flex)

        txt_slice2 = str(np_arr2[50:90,40:80])
        txt_slice_tot = txt_slice2
        self.image_loaded.emit(txt_slice_tot)


def get_experiments(experiment_path):
    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentListFactory.from_json_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.press_butt)

        self_v_layout = QVBoxLayout(self)
        self_v_layout.addWidget(self.button)
        '''
        imageLabel = QLabel()
        image = QImage("../../PyQt4_toys/tux_n_chrome.png")
        imageLabel.setPixmap( QPixmap.fromImage(image))
        self_v_layout.addWidget(imageLabel)
        '''

        self.img_label = QLabel("\n tmp dummy \n")
        self_v_layout.addWidget(self.img_label)

        self.img_num = 1

        self.setLayout(self_v_layout)
        self.show()

    def press_butt(self):

        self.lst_thread = []

        timer = QTimer(self)
        timer.timeout.connect(self.refresh_img)
        timer.start(200)

    def refresh_img(self):

        #"/scratch/30day_tmp/run_dui2_nodes/run1/imported.expt"
        #"/tmp/run_dui2_nodes/run1/imported.expt"
        #"/scratch/30day_tmp/nx_tst/run_dui2_nodes/run4/refined.expt"
        "/tmp/tst_ccp4_dials/run_dui2_nodes/run1/imported.expt"

        self.img_num += 1
        new_thread = LoadImages(
            path_in = "/tmp/tst_ccp4_dials/run_dui2_nodes/run1/imported.expt",
            img_num = self.img_num
        )
        new_thread.image_loaded.connect(self.update_text)
        self.lst_thread.append(new_thread)
        new_thread.start()

    def update_text(self, txt_slice_tot):
        self.img_label.setText(txt_slice_tot)

        print("Done")


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = MyWidget()
    myApp.exec_()
    sys.exit(0)
